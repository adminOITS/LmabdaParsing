from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class JobCategoryEnum(str, Enum):
    ACCOUNTING = "ACCOUNTING"
    ADMINISTRATIVE_ASSISTANT = "ADMINISTRATIVE_ASSISTANT"
    AGRICULTURE = "AGRICULTURE"
    ANIMATION = "ANIMATION"
    ART = "ART"
    ARTIFICIAL_INTELLIGENCE = "ARTIFICIAL_INTELLIGENCE"
    AUDIT = "AUDIT"
    BACKEND_DEVELOPMENT = "BACKEND_DEVELOPMENT"
    BIOTECHNOLOGY = "BIOTECHNOLOGY"
    BLOCKCHAIN = "BLOCKCHAIN"
    BTP = "BTP"
    BUSINESS_DEVELOPMENT = "BUSINESS_DEVELOPMENT"
    CATERING = "CATERING"
    CLOUD_COMPUTING = "CLOUD_COMPUTING"
    COMMERCIAL = "COMMERCIAL"
    COMMUNICATION = "COMMUNICATION"
    CONSTRUCTION = "CONSTRUCTION"
    CONTENT_CREATION = "CONTENT_CREATION"
    COPY_WRITING = "COPY_WRITING"
    CORPORATE_FINANCE = "CORPORATE_FINANCE"
    CUSTOMER_SERVICE = "CUSTOMER_SERVICE"
    CYBERSECURITY = "CYBERSECURITY"
    DATA_ANALYSIS = "DATA_ANALYSIS"
    DATA_ENTRY = "DATA_ENTRY"
    DATA_ENGINEERING = "DATA_ENGINEERING"
    DATA_SCIENCE = "DATA_SCIENCE"
    DELIVERY = "DELIVERY"
    DESIGN = "DESIGN"
    DIGITAL = "DIGITAL"
    DIGITAL_MARKETING = "DIGITAL_MARKETING"
    ECOMMERCE_ANALYTICS = "ECOMMERCE_ANALYTICS"
    ECOMMERCE_CUSTOMER_SERVICE = "ECOMMERCE_CUSTOMER_SERVICE"
    ECOMMERCE_MARKETING = "ECOMMERCE_MARKETING"
    ECOMMERCE_OPERATIONS = "ECOMMERCE_OPERATIONS"
    ECOMMERCE_SALES = "ECOMMERCE_SALES"
    ECOMMERCE_WEBSITE_MANAGEMENT = "ECOMMERCE_WEBSITE_MANAGEMENT"
    EDUCATION = "EDUCATION"
    ENERGY = "ENERGY"
    ENGINEERING = "ENGINEERING"
    ENTREPRENEURSHIP = "ENTREPRENEURSHIP"
    ENVIRONMENT = "ENVIRONMENT"
    EVENTS = "EVENTS"
    EVENTS_COORDINATION = "EVENTS_COORDINATION"
    EXTERNAL_AUDIT = "EXTERNAL_AUDIT"
    FINANCE = "FINANCE"
    FRONTEND_DEVELOPMENT = "FRONTEND_DEVELOPMENT"
    FULLSTACK_DEVELOPMENT = "FULLSTACK_DEVELOPMENT"
    GRAPHIC_DESIGN = "GRAPHIC_DESIGN"
    HEALTH = "HEALTH"
    HOSPITALITY = "HOSPITALITY"
    HUMAN_RESOURCES = "HUMAN_RESOURCES"
    INDUSTRIAL_PRODUCTION = "INDUSTRIAL_PRODUCTION"
    INFORMATION_TECHNOLOGY = "INFORMATION_TECHNOLOGY"
    INSURANCE = "INSURANCE"
    INTERPRETATION = "INTERPRETATION"
    IT = "IT"
    IT_PROJECT_MANAGEMENT = "IT_PROJECT_MANAGEMENT"
    LAW_ENFORCEMENT = "LAW_ENFORCEMENT"
    LEGAL = "LEGAL"
    LEGAL_ADVISORY = "LEGAL_ADVISORY"
    LOGISTICS = "LOGISTICS"
    MACHINE_LEARNING = "MACHINE_LEARNING"
    MANAGEMENT = "MANAGEMENT"
    MARKETING = "MARKETING"
    MEDICAL = "MEDICAL"
    MOBILE_DEVELOPMENT = "MOBILE_DEVELOPMENT"
    NETWORK_ADMINISTRATION = "NETWORK_ADMINISTRATION"
    NGO = "NGO"
    NURSING = "NURSING"
    OFFICE_MANAGEMENT = "OFFICE_MANAGEMENT"
    OTHER = "OTHER"
    PARAMEDICAL = "PARAMEDICAL"
    PHARMACEUTICAL = "PHARMACEUTICAL"
    PROCUREMENT = "PROCUREMENT"
    PRODUCT = "PRODUCT"
    PRODUCT_MANAGEMENT = "PRODUCT_MANAGEMENT"
    PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT"
    PUBLIC_RELATIONS = "PUBLIC_RELATIONS"
    PUBLIC_SECTOR = "PUBLIC_SECTOR"
    PURCHASING = "PURCHASING"
    QA_ENGINEERING = "QA_ENGINEERING"
    REAL_ESTATE = "REAL_ESTATE"
    RECRUITMENT = "RECRUITMENT"
    REMOTE = "REMOTE"
    SALES = "SALES"
    SALES_ADMINISTRATION = "SALES_ADMINISTRATION"
    SALES_SUPPORT = "SALES_SUPPORT"
    SCIENCE = "SCIENCE"
    SCIENTIFIC_RESEARCH = "SCIENTIFIC_RESEARCH"
    SHOPIFY_DEVELOPMENT = "SHOPIFY_DEVELOPMENT"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    SOCIAL_WORK = "SOCIAL_WORK"
    SOFTWARE_DEVELOPMENT = "SOFTWARE_DEVELOPMENT"
    SPORTS = "SPORTS"
    STRATEGY = "STRATEGY"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    SYSTEMS_ADMINISTRATION = "SYSTEMS_ADMINISTRATION"
    TECHNICAL_SUPPORT = "TECHNICAL_SUPPORT"
    TECHNICIAN = "TECHNICIAN"
    TELECOMMUNICATION = "TELECOMMUNICATION"
    TOURISM = "TOURISM"
    TRAINING = "TRAINING"
    TRANSLATION = "TRANSLATION"
    TRANSPORT = "TRANSPORT"
    UI_UX_DESIGN = "UI_UX_DESIGN"
    VIDEO_EDITING = "VIDEO_EDITING"
    VOLUNTEERING = "VOLUNTEERING"
    WAREHOUSING = "WAREHOUSING"
    WEB_DEVELOPMENT = "WEB_DEVELOPMENT"



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

class JobCategory(BaseModel):
    category: JobCategoryEnum = Field(..., description="domain , sector or category ")

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
    categories: List[JobCategory] = Field(..., description="List of job categories")
    


class Profile(BaseModel):
    profileTitle: str= Field(..., description="Professional title for the candidate that should has 5 word max")
    #profileCategory: Optional[str] = Field(None, description="Domain or sector (e.g., marketing, IT)")
    candidate: Candidate = Field(..., description="Structured candidate details")

