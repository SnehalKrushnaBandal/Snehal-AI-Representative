from fastapi import FastAPI
from pathlib import Path
from pypdf import PdfReader
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
import json

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

# ************ Part 3 : Creating system and user prompt  
class CharRequest_Class(BaseModel):
    question : str

def ask_candidate(question: str, resume: Resume_Class):
    sys_prompt = f"""
You are an AI assistant representing a job candidate.

Below is everything you know aout the candidate.

{resume.model_dump_json(indent=2)}

Rules: 
1. Answer only using this information.
2. Never hallucinate.
3. If information is unavilable , 
say:
"I don't have enough information to answer that."
4. Be professional.
5. Answer as if HR is interviewing this candidate. 
"""

    response = client.chat.completions.create(
        model=model, 
        messages = [
        {
        "role" : "system",
        "content" : sys_prompt
        }, 

        {
            "role" : "user",
            "content" : question
        }
        ]
    )
    return response.choices[0].message.content

# ************* Part 4 Home page 
@app.get("/")


def home():

    return {
        "message" : "resume parsed successfully"
    }

# ********** Part 5 Creating chat page
@app.post("/chat")

def chat(request: CharRequest_Class):
    resume_text = read_pdf_resume(Path("SnehalBandal_Resume.pdf"))
    
    resume = parse_resume(resume_text)
    answer = ask_candidate(request.question, resume)

    return {
        "answer" : answer
    }

