from llama_cloud_services import LlamaExtract
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum
import uuid

import json
import boto3
import os
import tempfile
import requests
import time
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
BUCKET_NAME = "job-sourcing-private-bucket-test-env"

CANDIDATE_SERVICE_URL = get_parameter("/llama/candidate_api_key", with_decryption=True)

extractor = LlamaExtract(api_key=API_KEY)


def update_status(track_id, status, reason=None):
    """Call API to update status."""
    url = f"{CANDIDATE_SERVICE_URL}/ai-processing-track/{track_id}/status/{status}"
    params = {}
    if reason:
        params['reason'] = reason
    try:
        response = requests.put(url, params=params, timeout=15)
        response.raise_for_status()
        logger.info(f"Updated status '{status}' for trackId={track_id}")
    except Exception as e:
        logger.error(f"Failed to update status '{status}' for trackId={track_id}: {e}")

# Define all Pydantic models (skip here for brevity — keep your original ones unchanged)


class Language(str, Enum):
    ENGLISH = "ENGLISH"
    FRENCH = "FRENCH"
    GERMAN = "GERMAN"
    SPANISH = "SPANISH"
    ITALIAN = "ITALIAN"
    PORTUGUESE = "PORTUGUESE"
    DUTCH = "DUTCH"
    SWEDISH = "SWEDISH"
    NORWEGIAN = "NORWEGIAN"
    DANISH = "DANISH"
    FINNISH = "FINNISH"
    ICELANDIC = "ICELANDIC"
    GREEK = "GREEK"
    POLISH = "POLISH"
    CZECH = "CZECH"
    SLOVAK = "SLOVAK"
    HUNGARIAN = "HUNGARIAN"
    ROMANIAN = "ROMANIAN"
    BULGARIAN = "BULGARIAN"
    CROATIAN = "CROATIAN"
    SERBIAN = "SERBIAN"
    BOSNIAN = "BOSNIAN"
    SLOVENE = "SLOVENE"
    ALBANIAN = "ALBANIAN"
    UKRAINIAN = "UKRAINIAN"
    RUSSIAN = "RUSSIAN"
    TURKISH = "TURKISH"
    ARABIC = "ARABIC"
    FULA = "FULA"
    HAUSA = "HAUSA"
    SWAHILI = "SWAHILI"
    SOMALI = "SOMALI"
    AMHARIC = "AMHARIC"
    YORUBA = "YORUBA"
    IGBO = "IGBO"
    ZULU = "ZULU"
    AFRIKAANS = "AFRIKAANS"
    TSWANA = "TSWANA"
    SHONA = "SHONA"
    BERBER = "BERBER"
    TAMIL = "TAMIL"           # diaspora in Africa and Europe
    URDU = "URDU"             # some presence in UK
    NOT_DEFINED = "NOT_DEFINED"

# Define Enums for strict value enforcement
class SkillProficiencyLevel(str, Enum):
    NOVICE = "NOVICE"
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"
    MASTER = "MASTER"

class LanguageProficiencyLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    NATIVE = "NATIVE"

# Define nested schema models
class Address(BaseModel):
    city: str=Field(..., description="City where the candidate resides default NOT_DEFINED")
    country: str=Field(..., description="Country where the candidate resides default NOT_DEFINED")
    zipCode: Optional[str]=Field(None, description="Postal or ZIP code") 
    addressLine1: Optional[str]=Field(None, description="Street address")
    state:Optional[str]=Field(None, description="state address")

class SocialLinks(BaseModel):
    githubUrl: Optional[str] = Field(None, description="GitHub profile URL")
    linkedinUrl: Optional[str] = Field(None, description="LinkedIn profile URL")
    portfolioUrl: Optional[str] = Field(None, description="Portfolio or personal website")
    otherUrl: Optional[str] = Field(None, description="Any other relevant link")

class Skill(BaseModel):
    name: str = Field(..., description="Name of the skill, e.g., Java, Spring Boot")
    proficiencyLevel: SkillProficiencyLevel = Field(..., description="Level of proficiency with the skill")

class Experience(BaseModel):
    jobTitle: str = Field(..., description="Candidate's job title, e.g., Software Engineer default NOT_DEFINED")
    company: str = Field(..., description="Company name")
    startDate: str = Field(..., description="Start date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    endDate: Optional[str] = Field(None, description="End date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    current: bool = Field(..., description="Whether this job is currently held")
    description: Optional[str] = Field(None, description="Brief summary of responsibilities and achievements")
    location: Optional[str] = Field(None, description="Job location (e.g., city)")
    industry: Optional[str] = Field(None, description="Industry sector, e.g., IT, Finance")


class Education(BaseModel):
    degree: str = Field(..., description="Degree earned, e.g., Bachelor, Master default NOT_DEFINED")
    field: str = Field(..., description="Field of study, e.g., Computer Science")
    institution: str = Field(..., description="Name of the educational institution")
    startDate: str = Field(..., description="Start date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    endDate: Optional[str] = Field(None, description="End date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    current: bool = Field(..., description="Is the education ongoing?")
    location: Optional[str] = Field(None, description="Location of the institution")


class Language(BaseModel):
    language: Language = Field(..., description="Name of the language, e.g., English default NOT_DEFINED")
    proficiencyLevel: LanguageProficiencyLevel = Field(..., description="Proficiency level in the language")

class Candidate(BaseModel):
    firstName: str = Field(..., description="Candidate's first name default NOT_DEFINED")
    lastName: str = Field(..., description="Candidate's last name default NOT_DEFINED")
    phone: Optional[str] = Field(None, description="Candidate's phone number default NOT_DEFINED")
    email: str = Field(..., description="Candidate's email address If an email appears in the résumé, return it exactly as written , If none is found {firstName_lower}.{lastName_lower}@not-defined.com use NOT_DEFINED when first/last name are unknown ")
    birthday: Optional[str] = Field(None, description="Birthdate Date (DD-MM-YYYY)")
    address: Optional[Address] = Field(None, description="Candidate's residential address")
    socialLinks: Optional[SocialLinks] = Field(None, description="Links to professional profiles")
    skills: List[Skill] = Field(..., description="List of candidate's skills")
    experiences: List[Experience] = Field(..., description="Professional experience entries")
    education: List[Education] = Field(..., description="Education background")
    languages: List[Language] = Field(..., description="Languages spoken and proficiency levels")
    categories: List[str] = Field(..., description="Domain or sector (e.g., marketing, IT")


class Profile(BaseModel):
    profileTitle: str= Field(..., description="Professional title for the candidate that should has 5 word max")
    #profileCategory: Optional[str] = Field(None, description="Domain or sector (e.g., marketing, IT)")
    candidate: Candidate = Field(..., description="Structured candidate details")


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
        update_status(track_id, "in-progress")

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
        candidate_api_url_generate_candidate_endpoint= f"{CANDIDATE_SERVICE_URL}/candidates/ai/ai-generator"
        response = requests.post(
            candidate_api_url_generate_candidate_endpoint,
            json=candidate_dict,
            headers={"Content-Type": "application/json"},
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
            update_status(track_id, "failed", reason=str(e))

        if 'local_path' in locals() and os.path.exists(local_path):
            os.remove(local_path)
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
