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

# Define all Pydantic models (skip here for brevity — keep your original ones unchanged)


class Language(str, Enum):
    ABKHAZIAN = "ABKHAZIAN"
    ACEH = "ACEH"
    ACHOLI = "ACHOLI"
    AFAR = "AFAR"
    AFRIKAANS = "AFRIKAANS"
    AKAN = "AKAN"
    ALBANIAN = "ALBANIAN"
    GERMAN = "GERMAN"
    ALUR = "ALUR"
    AMHARIC = "AMHARIC"
    ENGLISH = "ENGLISH"
    ARABIC = "ARABIC"
    ARMENIAN = "ARMENIAN"
    ASSAMESE = "ASSAMESE"
    AVAR = "AVAR"
    AWADHI = "AWADHI"
    AYMARA = "AYMARA"
    AZERBAIJANI = "AZERBAIJANI"
    BASHKIR = "BASHKIR"
    BALINESE = "BALINESE"
    BALOCHI = "BALOCHI"
    BAMBARA = "BAMBARA"
    BAOULE = "BAOULE"
    BASQUE = "BASQUE"
    BATAK_KARO = "BATAK_KARO"
    BATAK_SIMALUNGUN = "BATAK_SIMALUNGUN"
    BATAK_TOBA = "BATAK_TOBA"
    BEMBA = "BEMBA"
    BENGALI = "BENGALI"
    BETAVI = "BETAVI"
    BHOJPURI = "BHOJPURI"
    BELARUSIAN = "BELARUSIAN"
    BIKOL = "BIKOL"
    BURMESE = "BURMESE"
    BOSNIAN = "BOSNIAN"
    BURYAT = "BURYAT"
    BRETON = "BRETON"
    BULGARIAN = "BULGARIAN"
    CANTONESE = "CANTONESE"
    CATALAN = "CATALAN"
    CEBUANO = "CEBUANO"
    CHAMORRO = "CHAMORRO"
    CHEWA = "CHEWA"
    CHINESE_SIMPLIFIED = "CHINESE_SIMPLIFIED"
    CHINESE_TRADITIONAL = "CHINESE_TRADITIONAL"
    CHUUKESE = "CHUUKESE"
    SINHALA = "SINHALA"
    KOREAN = "KOREAN"
    CORSICAN = "CORSICAN"
    HAITIAN_CREOLE = "HAITIAN_CREOLE"
    MAURITIAN_CREOLE = "MAURITIAN_CREOLE"
    SEYCHELLOIS_CREOLE = "SEYCHELLOIS_CREOLE"
    CROATIAN = "CROATIAN"
    DANISH = "DANISH"
    DARI = "DARI"
    DINKA = "DINKA"
    DYULA = "DYULA"
    DOGRI = "DOGRI"
    DOMBE = "DOMBE"
    DZONGKHA = "DZONGKHA"
    SPANISH = "SPANISH"
    ESPERANTO = "ESPERANTO"
    ESTONIAN = "ESTONIAN"
    EWE = "EWE"
    FAROESE = "FAROESE"
    FIJIAN = "FIJIAN"
    FINNISH = "FINNISH"
    FON = "FON"
    FRENCH = "FRENCH"
    FRIULIAN = "FRIULIAN"
    WESTERN_FRISIAN = "WESTERN_FRISIAN"
    GA = "GA"
    SCOTTISH_GAELIC = "SCOTTISH_GAELIC"
    GALICIAN = "GALICIAN"
    WELSH = "WELSH"
    GANDA = "GANDA"
    GEORGIAN = "GEORGIAN"
    GUJARATI = "GUJARATI"
    GREEK = "GREEK"
    GREENLANDIC = "GREENLANDIC"
    GUARANI = "GUARANI"
    HAKHA_CHIN = "HAKHA_CHIN"
    HAUSA = "HAUSA"
    HAWAIIAN = "HAWAIIAN"
    HEBREW = "HEBREW"
    HILIGAYNON = "HILIGAYNON"
    HINDI = "HINDI"
    HMONG = "HMONG"
    HUNGARIAN = "HUNGARIAN"
    HUNSRICK = "HUNSRICK"
    YAKUT = "YAKUT"
    IBAN = "IBAN"
    IGBO = "IGBO"
    ILOCANO = "ILOCANO"
    INDONESIAN = "INDONESIAN"
    IRISH = "IRISH"
    ICELANDIC = "ICELANDIC"
    ITALIAN = "ITALIAN"
    JAPANESE = "JAPANESE"
    JAVANESE = "JAVANESE"
    JINGPO = "JINGPO"
    KANNADA = "KANNADA"
    KANURI = "KANURI"
    KAZAKH = "KAZAKH"
    KHASI = "KHASI"
    KHMER = "KHMER"
    KIGA = "KIGA"
    KIKONGO = "KIKONGO"
    KINYARWANDA = "KINYARWANDA"
    KYRGYZ = "KYRGYZ"
    KITUBA = "KITUBA"
    KOK_BOROK = "KOK_BOROK"
    KOMI = "KOMI"
    KONKANI = "KONKANI"
    KRIO = "KRIO"
    KURDISH = "KURDISH"
    LAO = "LAO"
    LATGALIAN = "LATGALIAN"
    LATIN = "LATIN"
    LATVIAN = "LATVIAN"
    LIGURIAN = "LIGURIAN"
    LIMBURGISH = "LIMBURGISH"
    LINGALA = "LINGALA"
    LITHUANIAN = "LITHUANIAN"
    LOMBARD = "LOMBARD"
    LUO = "LUO"
    LUSHAI = "LUSHAI"
    LUXEMBOURGISH = "LUXEMBOURGISH"
    MACEDONIAN = "MACEDONIAN"
    MADURESE = "MADURESE"
    MAITHILI = "MAITHILI"
    MAKASSAR = "MAKASSAR"
    MALAY = "MALAY"
    MALAY_ARABIC = "MALAY_ARABIC"
    MALAYALAM = "MALAYALAM"
    DHIVEHI = "DHIVEHI"
    MALAGASY = "MALAGASY"
    MALTESE = "MALTESE"
    MAM = "MAM"
    MANIPURI = "MANIPURI"
    MANX = "MANX"
    MAORI = "MAORI"
    MARATHI = "MARATHI"
    MEADOW_MARI = "MEADOW_MARI"
    MARSHALLESE = "MARSHALLESE"
    MARWARI = "MARWARI"
    YUCATEC_MAYA = "YUCATEC_MAYA"
    MINANGKABAU = "MINANGKABAU"
    MONGOLIAN = "MONGOLIAN"
    NKO = "NKO"
    NAHUATL = "NAHUATL"
    NDAU = "NDAU"
    SOUTH_NDEBELE = "SOUTH_NDEBELE"
    DUTCH = "DUTCH"
    NEPALI = "NEPALI"
    NEWARI = "NEWARI"
    NORWEGIAN = "NORWEGIAN"
    NUER = "NUER"
    OCCITAN = "OCCITAN"
    ODIA = "ODIA"
    OROMO = "OROMO"
    OSSETIC = "OSSETIC"
    UDMURT = "UDMURT"
    UYGHUR = "UYGHUR"
    URDU = "URDU"
    UZBEK = "UZBEK"
    PASHTO = "PASHTO"
    PAMPANGAN = "PAMPANGAN"
    PANGASINAN = "PANGASINAN"
    PAPIAMENTO = "PAPIAMENTO"
    JAMAICAN_PATOIS = "JAMAICAN_PATOIS"
    PUNJABI = "PUNJABI"
    PUNJABI_ARABIC = "PUNJABI_ARABIC"
    PERSIAN = "PERSIAN"
    FULA = "FULA"
    POLISH = "POLISH"
    PORTUGUESE = "PORTUGUESE"
    PORTUGUESE_PORTUGAL = "PORTUGUESE_PORTUGAL"
    QEQCHI = "QEQCHI"
    QUECHUA = "QUECHUA"
    ROMANI = "ROMANI"
    ROMANIAN = "ROMANIAN"
    RUNDI = "RUNDI"
    RUSSIAN = "RUSSIAN"
    NORTHERN_SAMI = "NORTHERN_SAMI"
    SAMOAN = "SAMOAN"
    SANGO = "SANGO"
    SANSKRIT = "SANSKRIT"
    SANTALI = "SANTALI"
    SERBIAN = "SERBIAN"
    SHAN = "SHAN"
    SHONA = "SHONA"
    SICILIAN = "SICILIAN"
    SILESIAN = "SILESIAN"
    SINDHI = "SINDHI"
    SLOVAK = "SLOVAK"
    SLOVENE = "SLOVENE"
    SOMALI = "SOMALI"
    SORANI = "SORANI"
    NORTHERN_SOTHO = "NORTHERN_SOTHO"
    SOUTHERN_SOTHO = "SOUTHERN_SOTHO"
    SUNDANESE = "SUNDANESE"
    SUSU = "SUSU"
    SWEDISH = "SWEDISH"
    SWAHILI = "SWAHILI"
    SWATI = "SWATI"
    TAJIK = "TAJIK"
    TAGALOG = "TAGALOG"
    TAHITIAN = "TAHITIAN"
    TAMAZIGHT = "TAMAZIGHT"
    TAMAZIGHT_TIFINAGH = "TAMAZIGHT_TIFINAGH"
    TAMIL = "TAMIL"
    TATAR = "TATAR"
    CRIMEAN_TATAR = "CRIMEAN_TATAR"
    CZECH = "CZECH"
    CHECHEN = "CHECHEN"
    CHUVASH = "CHUVASH"
    TELUGU = "TELUGU"
    TETUM = "TETUM"
    THAI = "THAI"
    TIBETAN = "TIBETAN"
    TIGRINYA = "TIGRINYA"
    TIV = "TIV"
    TOK_PISIN = "TOK_PISIN"
    TONGAN = "TONGAN"
    TULU = "TULU"
    TUVAN = "TUVAN"
    TSONGA = "TSONGA"
    TSWANA = "TSWANA"
    TUMBUKA = "TUMBUKA"
    TURKISH = "TURKISH"
    TURKMEN = "TURKMEN"
    UKRAINIAN = "UKRAINIAN"
    VENDA = "VENDA"
    VENETIAN = "VENETIAN"
    VIETNAMESE = "VIETNAMESE"

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
    city: str=Field(..., description="City where the candidate resides")
    country: str
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
    jobTitle: str = Field(..., description="Candidate's job title, e.g., Software Engineer")
    company: str = Field(..., description="Company name")
    startDate: str = Field(..., description="Start date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    endDate: Optional[str] = Field(None, description="End date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    current: bool = Field(..., description="Whether this job is currently held")
    description: Optional[str] = Field(None, description="Brief summary of responsibilities and achievements")
    location: Optional[str] = Field(None, description="Job location (e.g., city)")
    industry: Optional[str] = Field(None, description="Industry sector, e.g., IT, Finance")


class Education(BaseModel):
    degree: str = Field(..., description="Degree earned, e.g., Bachelor, Master")
    field: str = Field(..., description="Field of study, e.g., Computer Science")
    institution: str = Field(..., description="Name of the educational institution")
    startDate: str = Field(..., description="Start date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    endDate: Optional[str] = Field(None, description="End date (formats: DD-MM-YYYY, MM-YYYY, or YYYY)")
    current: bool = Field(..., description="Is the education ongoing?")
    location: Optional[str] = Field(None, description="Location of the institution")


class Language(BaseModel):
    language: Language = Field(..., description="Name of the language, e.g., English")
    proficiencyLevel: LanguageProficiencyLevel = Field(..., description="Proficiency level in the language")

class Candidate(BaseModel):
    firstName: str = Field(..., description="Candidate's first name")
    lastName: str = Field(..., description="Candidate's last name")
    phone: Optional[str] = Field(None, description="Candidate's phone number")
    email: str = Field(..., description="Candidate's email address")
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



def lambda_handler(event, context):
    try:
        logger.info("Lambda invoked")
        # 1. Parse request body
        body = json.loads(event.get('body', '{}'))
        logger.info("Request body parsed: %s", body)
        required_fields = ['key', 'fileName', 'size', 'contentType']
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

        # 3. Delete all existing agents first
        logger.info("Listing existing agents...")
        existing_agents = extractor.list_agents()
        if len(existing_agents) >= 2:
            for agent_info in existing_agents:
                try:
                    extractor.delete_agent(agent_info.id)
                    logger.info("Deleted agent: %s", agent_info.id)
                except Exception as delete_err:
                    logger.warning("Failed to delete agent %s: %s", agent_info.id, str(delete_err))

        # 4. Create new agent
        agent_name = f"resume-parser-{uuid.uuid4()}"
        logger.info("Creating new agent: %s", agent_name)
        agent = extractor.create_agent(name=agent_name, data_schema=Profile)
        logger.info("Agent created: %s", agent.id)

        # 5. Extract data
        logger.info("Extracting resume data...")
        result = agent.extract(local_path)
        candidate_dict = result.data
        
        logger.info("*******************************************************************")
        logger.info("Resume data extracted.%s",candidate_dict)

        # 6. Add resume metadata
        resumeAttachment = {
            "fileName": body.get("fileName"),
            "contentType": body.get("contentType"),
            "size": body.get("size"),
            "key": body.get("key")
        }
        candidate_dict["resumeAttachment"] = resumeAttachment
        logger.info("Resume metadata added.")

        # 7. Delete temp file
        if os.path.exists(local_path):
            os.remove(local_path)
            logger.info("Temporary file deleted: %s", local_path)


        # 9. Send result to candidate service
        logger.info("Sending extracted data to candidate service...")
        response = requests.post(
            CANDIDATE_SERVICE_URL,
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
        if 'local_path' in locals() and os.path.exists(local_path):
            os.remove(local_path)
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
