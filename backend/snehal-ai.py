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
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Error")

client = Groq(api_key=my_api_key)
# model = "openai/gpt-oss-20b"
model = "openai/gpt-oss-120b"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

1. Answer only using the supplied information.
2. Never invent information.
3. If the information is unavailable, say:
   "I don't have enough information to answer that."
4. Be professional and factual.
5. Answer as if you are representing the candidate.
6. Do not assume information that is not present.
7. Do not confuse technologies mentioned in projects with technologies
   the candidate claims as their strongest skills.
8. Keep answers concise and recruiter-friendly.
9. Prefer short paragraphs or bullet points for lists.
10. Do not use Markdown tables unless the recruiter explicitly asks
    for a comparison or tabular format.
11. Do not create unnecessary headings or long explanations.
12. For simple factual questions, answer directly in 1-4 sentences.
13. For questions about strengths, skills, hobbies, education,
    experience, or projects, use bullet points when multiple items
    are needed.

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

    question = question.lower().strip()

# =========================
# PROJECTS
# =========================

    projects = candidate_profile["projects"]

    if any(term in question for term in [
        "legallens",
        "legal lens",
        "text extraction",
        "extract text",
        "text extracted",
        "ocr",
        "how text is extracted",
        "how is text extracted",
        "database",
        "databases",
        "technology used",
        "technologies used",
        "tech stack",
        "tech stack used",
        "tools used",
        "framework used",
        "frameworks used",
        "which technologies",
        "which technology"
    ]):
        for project in projects:
            if project.get("name", "").lower() == "legallens":
                return {
                    "project": project
                }

    if any(term in question for term in [
        "fitness tracking",
        "fitness project",
        "ai fitness"
    ]):
        for project in projects:
            if "fitness" in project.get("name", "").lower():
                return {
                    "project": project
                }

    if any(term in question for term in [
        "resume screening",
        "resume screening system"
    ]):
        for project in projects:
            if "resume screening" in project.get("name", "").lower():
                return {
                    "project": project
                }

    if any(term in question for term in [
        "cafe management",
        "cafe project"
    ]):
        for project in projects:
            if "cafe" in project.get("name", "").lower():
                return {
                    "project": project
                }

    if any(term in question for term in [
        "stegoai",
        "stego ai"
    ]):
        for project in projects:
            if "stegoai" in project.get("name", "").lower():
                return {
                    "project": project
                }

    if any(term in question for term in [
        "project",
        "projects",
        "explain project",
        "explain the project",
        "project in detail",
        "explain project in detail",
        "project details",
        "project overview"
    ]):
        return {
            "projects": projects
        }


    # =========================
    # STRENGTHS
    # =========================
    if any(term in question for term in [
        "strength",
        "strengths"
    ]):
        return {
            "strengths": candidate_profile["strengths"]
        }

    # =========================
    # WEAKNESS
    # =========================
    if any(term in question for term in [
        "weakness",
        "weaknesses"
    ]):
        return {
            "hr_profile": {
                "weakness": candidate_profile["hr_profile"].get("weakness")
            }
        }

    # =========================
    # HR QUESTIONS
    # =========================
    if any(term in question for term in [
        "pressure",
        "deadline",
        "teamwork",
        "team",
        "failure",
        "conflict",
        "achievement",
        "challenge"
    ]):
        return {
            "hr_profile": candidate_profile["hr_profile"]
        }

    # =========================
    # EXPERIENCE
    # =========================
    if any(term in question for term in [
        "experience",
        "internship experience",
        "internships",
        "worked at",
        "previous role",
        "previous company",
        "work experience"
    ]):
        return {
            "experience": candidate_profile["experience"]
        }

    # =========================
    # CAREER
    # =========================
    if any(term in question for term in [
        "career goal",
        "career goals",
        "career",
        "motivation",
        "why it",
        "why information technology",
        "why software",
        "why software development"
    ]):
        return {
            "professional_profile": candidate_profile["professional_profile"]
        }

    # =========================
    # WORK PREFERENCES
    # =========================
    if any(term in question for term in [
        "relocate",
        "relocation",
        "preferred location",
        "preferred locations",
        "work location",
        "remote",
        "hybrid",
        "onsite",
        "full time",
        "full-time",
        "availability",
        "joining"
    ]):
        return {
            "work_preferences": candidate_profile["work_preferences"]
        }

    # =========================
    # EDUCATION
    # =========================
    if any(term in question for term in [
        "education",
        "college",
        "degree",
        "cgpa",
        "graduation",
        "graduation year",
        "graduate",
        "diploma",
        "school",
        "study"
    ]):
        return {
            "basic_profile": candidate_profile["basic_profile"],
            "education": candidate_profile["education"]
        }

    # =========================
    # TECHNICAL SKILLS
    # =========================
    if any(term in question for term in [
        "skill",
        "skills",
        "technology",
        "technologies",
        "java",
        "python",
        "react",
        "node.js",
        "node",
        "spring boot",
        "spring",
        "database",
        "backend",
        "frontend",
        "cloud"
    ]):
        return {
            "technical_profile": candidate_profile["technical_profile"]
        }

    # =========================
    # PERSONAL
    # =========================
    if any(term in question for term in [
        "hobby",
        "hobbies",
        "interest",
        "interests",
        "free time"
    ]):
        return {
            "personal_profile": candidate_profile["personal_profile"]
        }

    # =========================
    # DEFAULT
    # =========================
    return {
        "basic_profile": candidate_profile["basic_profile"]
    }

# =========================
# Part 3 : Creating system and user prompt
# =========================

class ChatMessage_Class(BaseModel):
    role: str
    content: str


class ChatRequest_Class(BaseModel):
    question: str
    history: list[ChatMessage_Class] = []


def build_candidate_system_prompt(
    question: str,
    resume: Resume_Class,
    relevant_profile: dict
):

    return f"""
You are Snehal AI, the AI-powered developer representative of
Snehal Krushna Bandal.

Your job is to answer questions about Snehal using ONLY the
relevant candidate information supplied below.

=== RELEVANT CANDIDATE PROFILE ===

{json.dumps(relevant_profile, indent=2)}

=== STRICT RULES ===

1. Use ONLY the information provided above.

2. Never invent, assume, or infer facts that are not explicitly provided.

3. Give the most direct answer to the question.

4. Keep normal answers concise, usually 1-4 sentences.

5. Do not provide a long explanation unless the recruiter explicitly
asks for details.

6. Do not include information from unrelated sections.

7. Do not turn a simple question into a complete candidate summary.

8. If the information is not available, say exactly:

"I don't have enough information to answer that."

9. When listing multiple items, use short bullet points.

10. Do not create fictional examples or experiences.

11. Do not add a GitHub link unless the recruiter asks for it.

12. Represent Snehal professionally and factually.


=== PROJECT RULES ===

=== PROJECT RULES ===

13. When the question is about a specific project, answer only about
that requested project.

14. Do not describe other projects unless the recruiter asks for
a comparison.

15. For "What is..." or "Tell me about..." questions, give a concise
project overview.

16. For "Explain..." or "in detail" questions, provide a structured
but focused explanation.

17. When explaining a project in detail, cover only the information
available in the project profile, such as:
- Project purpose
- Problem being solved
- Main features
- Technologies used
- How the system works
- AI/OCR components
- Database
- Outcome or purpose

18. Do not invent technical details that are not present in the
candidate profile.

19. For questions about one specific aspect such as technologies,
database, OCR, features, or challenges, answer only that aspect.

20. Do not provide information about unrelated projects.

=== ANSWER STYLE ===

Simple factual question:
Give a short direct answer.

Strength question:
Give only the actual strengths from the candidate profile.

Project question:
Give the project name and a short description first.

HR question:
Use the relevant HR information directly and keep the response concise.

Answer the recruiter's question directly.
"""

def ask_candidate(
    question: str,
    resume: Resume_Class,
    candidate_profile: dict,
    history: list[ChatMessage_Class]
):

    relevant_profile = get_relevant_profile(
        question,
        candidate_profile
    )

    sys_prompt = build_candidate_system_prompt(
        question,
        resume,
        relevant_profile
    )

  
    messages = [
    {
        "role": "system",
        "content": sys_prompt
    }
    ]

    for message in history:
        messages.append({
            "role": message.role,
            "content": message.content
        })

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    

    return response.choices[0].message.content


# *********** Streaming answer
def stream_candidate_answer(
    question: str,
    resume: Resume_Class,
    candidate_profile: dict,
    history: list[ChatMessage_Class]
):

    relevant_profile = get_relevant_profile(
        question,
        candidate_profile
    )

    sys_prompt = build_candidate_system_prompt(
        question,
        resume,
        relevant_profile
    )

    messages = [
        {
            "role": "system",
            "content": sys_prompt
        }
    ]

    for message in history:
        messages.append({
            "role": message.role,
            "content": message.content
        })

    messages.append({
        "role": "user",
        "content": question
    })

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
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

    answer = ask_candidate( request.question, resume, candidate_profile, request.history )

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
            candidate_profile,
            request.history
        ),
        media_type="text/plain"
    )