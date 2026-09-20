from fastapi import FastAPI
from pathlib import Path
from pypdf import PdfReader
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
import json
from fastapi.responses import StreamingResponse
from services.candidate_service import load_candidate_profile

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Error")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

app = FastAPI()

# ************ Part 1 
# 1. Pdf Extraction
def read_pdf_resume(file_path : Path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if(page_text):
            text += page_text + "\n"
    return text

# ************ Part 2
# 2. Parsing Resume 
def parse_resume(resume_text):

    system_prompt = f"""
You are an expert resume parser.

Extract information from the resume based on its meaning, not only based on exact section headings.

Different resumes may use different headings.

For example: 
- Experince
- Professional Experince
- Work History
- Employment
- Internships

These may all contain relevant experince.

Skills may appear in:
- Skills section
- Work experience
- Internships
- Projects

Return ONLY valid JSON matching this schema: 
{resume_schema} 

Important rules: 

1. Do not invent information.
2. If a value is not available, return null.
3. If a list has no information, return an empty list.
4. Include internships inside experiences.
5. Extract skills mentioned across the entire resume.
6. Return ONLY the JSON object.
7. Do not use markdown.
8. Do not add explanations before or after the JSON.
"""

    user_prompt = f"""
        Parse the following resume: 
        {resume_text}
    """

    system_msg = {
        "role" : "system",
        "content" : system_prompt
    }

    user_msg = {
        "role" : "user",
        "content" : user_prompt
    }

    messages = [system_msg, user_msg]

    response_format = {
        "type" : "json_object"
    }

    response = client.chat.completions.create(model = model, messages = messages, response_format = response_format)

    raw_output = response.choices[0].message.content
    # print("\nRAW RESUME OUTPUT:")
    # print(raw_output)
    
    data = json.loads(raw_output)
    resume = Resume_Class(**data)
    return resume

class MatchDetails_Class(BaseModel):
    candidate_name: str
    matching_skills: list[str]
    missing_skills: list[str]
    experience_requirement_met: bool
    overall_match_percentage: float
    final_verdict: str

class MatchResult_Class(BaseModel):
    score : float
    details : MatchDetails_Class

# 1 : This experience is created just to use in Resume_Class
class Experience_Class(BaseModel):
    company : str | None = None
    role : str | None = None
    duration : str | None = None
    description : str | None = None
    skills_used : list[str] = []

# 2 : Main Resume_Class
class Resume_Class(BaseModel):
    name : str | None = None
    email : str | None = None
    phone : str | None = None

    total_experience_years : float | None = None
    skills : list[str] = []
    experiences : list[Experience_Class] = []
    education : list[str] = []
    projects : list[str] = []
    certifications : list[str] = []
    achievements : list[str] = []

# 3
resume_schema = Resume_Class.model_json_schema()


def get_relevant_profile(question: str, candidate_profile: dict):

    question = question.lower()

    if any(word in question for word in [
        "hobby",
        "hobbies",
        "interest",
        "interests",
        "free time",
        "personal"
    ]):
        return {
            "personal_profile": candidate_profile["personal_profile"]
        }

    if any(word in question for word in [
        "strength",
        "strengths",
        "weakness",
        "pressure",
        "deadline",
        "teamwork",
        "team",
        "failure",
        "conflict",
        "achievement",
        "challenge",
        "introduction"
    ]):
        return {
            "strengths": candidate_profile["strengths"],
            "hr_profile": candidate_profile["hr_profile"]
        }

    if any(word in question for word in [
        "career",
        "goal",
        "goals",
        "motivation",
        "why it",
        "why information technology",
        "why software",
        "software development"
    ]):
        return {
            "professional_profile": candidate_profile["professional_profile"]
        }

    if any(word in question for word in [
        "relocate",
        "relocation",
        "location",
        "remote",
        "hybrid",
        "onsite",
        "internship",
        "full time",
        "availability",
        "joining"
    ]):
        return {
            "work_preferences": candidate_profile["work_preferences"]
        }

    if any(word in question for word in [
        "project",
        "projects",
        "legallens",
        "fitness",
        "resume screening",
        "cafe",
        "stego"
    ]):
        return {
            "projects": candidate_profile["projects"]
        }

    if any(word in question for word in [
        "skill",
        "skills",
        "technology",
        "technologies",
        "java",
        "python",
        "react",
        "node",
        "spring",
        "database",
        "backend",
        "frontend",
        "ai",
        "cloud"
    ]):
        return {
            "technical_profile": candidate_profile["technical_profile"]
        }

    if any(word in question for word in [
        "education",
        "college",
        "degree",
        "cgpa",
        "diploma",
        "school",
        "study"
    ]):
        return {
            "basic_profile": candidate_profile["basic_profile"],
            "education": candidate_profile["education"]
        }

    # Default context for general questions
    return {
        "basic_profile": candidate_profile["basic_profile"],
        "professional_profile": candidate_profile["professional_profile"]
    }

# ************ Part 3 : Creating system and user prompt  
class ChatRequest_Class(BaseModel):
    question : str

def ask_candidate(
    question: str,
    resume: Resume_Class,
    candidate_profile: dict
):

    relevant_profile = get_relevant_profile(
        question,
        candidate_profile
    )

    sys_prompt = f"""
You are an AI assistant representing Snehal Krushna Bandal.

You are answering questions about the candidate using the information
provided below.

=== RESUME DATA ===

{resume.model_dump_json(indent=2)}

=== RELEVANT CANDIDATE PROFILE ===

{json.dumps(relevant_profile, indent=2)}

=== RULES ===

1. Answer only using the supplied information.
2. Never invent information.
3. If the information is unavailable, say:
   "I don't have enough information to answer that."
4. Be professional and factual.
5. Answer as if you are representing the candidate.
6. Do not assume information that is not present.
7. Do not confuse technologies mentioned in projects with technologies
   the candidate claims as their strongest skills.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content

# *********** Streaming answer
def stream_candidate_answer(
    question: str,
    resume: Resume_Class,
    candidate_profile: dict
):

    relevant_profile = get_relevant_profile(
        question,
        candidate_profile
    )

    sys_prompt = f"""
You are an AI assistant representing Snehal Krushna Bandal.

You are answering questions about the candidate using the information
provided below.

=== RESUME DATA ===

{resume.model_dump_json(indent=2)}

=== RELEVANT CANDIDATE PROFILE ===

{json.dumps(relevant_profile, indent=2)}

=== RULES ===

1. Answer only using the supplied information.
2. Never invent information.
3. If the information is unavailable, say:
   "I don't have enough information to answer that."
4. Be professional and factual.
5. Answer as if you are representing the candidate.
6. Do not assume information that is not present.
7. Do not confuse technologies mentioned in projects with technologies
   the candidate claims as their strongest skills.
"""

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        stream=True
    )
    for chunk in stream:

        content = chunk.choices[0].delta.content

        if content:
            yield content

RESUME_PATH = Path("SnehalBandal_Resume.pdf")
PROFILE_PATH = Path("candidate_profile.json")

resume_text = read_pdf_resume(RESUME_PATH)
resume = parse_resume(resume_text)

candidate_profile = load_candidate_profile(PROFILE_PATH)

# ************* Part 4 Home page 
@app.get("/")


def home():

    return {
        "message" : "resume parsed successfully"
    }

# ********** Part 5 Creating chat page
@app.post("/chat")
def chat(request: ChatRequest_Class):

    answer = ask_candidate( request.question, resume, candidate_profile )

    return {
        "answer": answer
    }

# ********** Part 6 Creating streaming chat
@app.post("/chat/stream")
def chat_stream(request: ChatRequest_Class):

    return StreamingResponse(
        stream_candidate_answer(
            request.question,
            resume,
            candidate_profile
        ),
        media_type="text/plain"
    )