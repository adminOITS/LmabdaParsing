from llama_cloud_services import LlamaExtract

import json
import boto3
import os
import tempfile
import requests
from dtos import Profile
import json

import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize client
# Retrieve parameters from SSM
ssm = boto3.client("ssm")

def get_parameter(name, with_decryption=False):
    return ssm.get_parameter(Name=name, WithDecryption=with_decryption)["Parameter"]["Value"]

# Fetch credentials from SSM
API_KEY = get_parameter("/llama/api_key", with_decryption=True)
CLIENT_SECRET_KEYCLOAK=get_parameter("/llama/client_secret_keycloak", with_decryption=True)
BUCKET_NAME = "job-sourcing-private-bucket-test-env"

GATE_WAY_URL = get_parameter("/jobsourcing/env/dev/gateway/url")
CANDIDATE_SERVICE_URL=GATE_WAY_URL+"/CANDIDATE-SERVICE/api/v1/candidates"

extractor = LlamaExtract(api_key=API_KEY)


def update_status(track_id, status,headers,reason=None,throwbel=True):
    """Call API to update status."""
    url = f"{CANDIDATE_SERVICE_URL}/ai-processing/{track_id}/status/{status}"
    params = {}
    if reason:
        params['reason'] = reason
    if throwbel:
        response = requests.put(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        logger.info(f"Updated status '{status}' for trackId={track_id}")
    else:
        try:
            response = requests.put(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            logger.info(f"Updated status '{status}' for trackId={track_id}")
        except Exception as e:
            logger.error(f"Failed to update status '{status}' for trackId={track_id}: {e}")

def get_access_token():
    token_url = "https://job-sourcing.com/realms/jobsourcingrealm/protocol/openid-connect/token"
    client_id = "lamdaParsingAiClient"
    client_secret = CLIENT_SECRET_KEYCLOAK

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    return response.json()["access_token"]


def get_or_create_agent(name: str, schema):
    agents = extractor.list_agents()
    for agent in agents:
        if agent.name == name:
            logger.info(f"Found existing agent: {name}")
            return agent

    # Agent not found — create it
    logger.info(f"Agent '{name}' not found. Creating a new one...")
    agent = extractor.create_agent(name=name, data_schema=schema)
    logger.info(f"Agent '{name}' created successfully.")
    return agent




def lambda_handler(event, context):
    
    try:
        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        logger.info("Lambda invoked")
        # Only one record expected per invocation
        record = event["Records"][0]
        body = json.loads(record["body"])
        logger.info("Processing SQS message: %s", body)

        required_fields = ['key','entityId']
        missing_fields = [field for field in required_fields if not body.get(field)]

        if missing_fields:
            logger.warning("Missing required fields: %s", missing_fields)
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": f"The following fields are required and must not be empty: {', '.join(missing_fields)}"
                })
            }

        key = body.get("key")
        logger.info("S3 key: %s", key)


        logger.info("Downloading file from S3...")
        # 2. Download file from S3
        s3 = boto3.client("s3")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            s3.download_fileobj(BUCKET_NAME, key, tmp_file)
            local_path = tmp_file.name
        
        logger.info("File downloaded to temporary path: %s", local_path)

        track_id = body.get("entityId")  # AI processing track ID
        # Mark the processing as IN_PROGRESS
        update_status(track_id, "in-progress",headers)

        # 4. Create new agent
        agent = get_or_create_agent("resume-parser-1", Profile)
        # 5. Extract data
        logger.info("Extracting resume data...")
        result = agent.extract(local_path)
        candidate_dict = result.data
        
        logger.info("*******************************************************************")
        logger.info("Resume data extracted.%s",candidate_dict)

        # 6. Add only the entityId  (the track Id ) to candidate data
        candidate_dict["entityId"] = body.get("entityId")
        logger.info("Entity ID added to candidate data: %s", candidate_dict["entityId"])

        # 7. Delete temp file
        if os.path.exists(local_path):
            os.remove(local_path)
            logger.info("Temporary file deleted: %s", local_path)


        # 9. Send result to candidate service
        logger.info("Sending extracted data to candidate service...")
        candidate_api_url_generate_candidate_endpoint= f"{CANDIDATE_SERVICE_URL}/ai"
        response = requests.post(
            candidate_api_url_generate_candidate_endpoint,
            json=candidate_dict,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        logger.info("Candidate data successfully sent. Response: %s", response.text)

        return {
            "statusCode": 200,
            "body": json.dumps(response.json())
        }

    except Exception as e:
        logger.error(f"Error processing resume: {e}")

        # Attempt to mark processing as FAILED if trackId available in body
        track_id = None
        try:
            record = event["Records"][0]
            body = json.loads(record["body"])
            track_id = body.get("entityId")
        except Exception:
            pass

        if track_id:
            token = get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            update_status(track_id, "failed", headers,reason=str(e),throwbel=False)

        if 'local_path' in locals() and os.path.exists(local_path):
            os.remove(local_path)
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
