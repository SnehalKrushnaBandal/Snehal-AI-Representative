import { useState } from "react";

import AIChat from "./components/AIChat";
import {
  ArrowUpRight,
  Bot,
  BriefcaseBusiness,
  Code2,
  GraduationCap,
  Home,
  MessageCircle,
  FileText,
  MapPin,
  Sparkles,
  ChevronRight,
} from "lucide-react";
import { FaGithub, FaLinkedinIn } from "react-icons/fa";
import "./App.css";

function App() {
  const [activeView, setActiveView] = useState("home");

  const [initialQuestion, setInitialQuestion] = useState("");
  const [showAllProjects, setShowAllProjects] = useState(false);

  const openProjectInAI = (question) => {
    setInitialQuestion(question);
    setActiveView("ai");
  };

  if (activeView === "ai") {
    return (
      <AIChat
        onBack={() => setActiveView("home")}
        initialQuestion={initialQuestion}
      />
    );
  }

  return (
    <div className="app">
      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">✦</div>
          <span>SNEHAL.AI</span>
        </div>

        <div className="sidebar-profile">
          <div className="profile-avatar">SB</div>

          <div>
            <h3>Snehal Bandal</h3>
            <p>Full Stack Developer</p>
          </div>
        </div>

        <nav className="navigation">
          <div className="nav-section">
            <span className="nav-label">OVERVIEW</span>

            <button
              className="nav-item active"
              onClick={() =>
                window.scrollTo({
                  top: 0,
                  behavior: "smooth",
                })
              }
            >
              <Home size={17} />
              <span>Overview</span>
            </button>
          </div>

          <div className="nav-section">
            <span className="nav-label">PROFILE</span>

            <button
              className="nav-item"
              onClick={() =>
                document
                  .getElementById("skills")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              <Code2 size={17} />
              <span>Skills</span>
            </button>

            <button
              className="nav-item"
              onClick={() =>
                document
                  .getElementById("experience")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              <BriefcaseBusiness size={17} />
              <span>Experience</span>
            </button>

            <button
              className="nav-item"
              onClick={() =>
                document
                  .getElementById("education")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              <GraduationCap size={17} />
              <span>Education</span>
            </button>
          </div>

          <div className="nav-section">
            <span className="nav-label">WORK</span>

            <button
              className="nav-item"
              onClick={() =>
                document
                  .getElementById("projects")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              <Code2 size={17} />
              <span>Projects</span>
            </button>
          </div>

          <div className="nav-section">
            <span className="nav-label">AI</span>

            <button
              className="nav-item ai-item"
              onClick={() => setActiveView("ai")}
            >
              <Sparkles size={17} />
              <span>Ask Snehal AI</span>
            </button>

            <button className="nav-item" onClick={() => setActiveView("ai")}>
              <Bot size={17} />
              <span>Recruiter Mode</span>
            </button>
          </div>
        </nav>

        <div className="sidebar-bottom">
        <div className="social-links">

  <a
    href="https://github.com/SnehalKrushnaBandal"
    target="_blank"
    rel="noreferrer"
    aria-label="GitHub"
  >
    <FaGithub size={16} />
  </a>

  <a
    href="https://www.linkedin.com/in/snehal-bandal-514592267"
    target="_blank"
    rel="noreferrer"
    aria-label="LinkedIn"
  >
    <FaLinkedinIn size={16} />
  </a>

  <a
    href="/SnehalBandal_Resume.pdf"
    target="_blank"
    rel="noreferrer"
    aria-label="Resume"
  >
    <FileText size={16} />
  </a>

</div>
        </div>
      </aside>

      {/* ================= MAIN CONTENT ================= */}

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="topbar-label">
              AI-POWERED DEVELOPER REPRESENTATIVE
            </span>
          </div>

          <div className="topbar-links">
            <a href="#" target="_blank">
              Resume
            </a>
            <a href="https://github.com/SnehalKrushnaBandal" target="_blank">
              GitHub ↗
            </a>
            <a
              href="https://www.linkedin.com/in/snehal-bandal-514592267/"
              target="_blank"
            >
              LinkedIn ↗
            </a>
          </div>
        </header>

        {/* ================= HERO ================= */}

        <section className="hero">
          <div className="hero-content">
            <span className="eyebrow">FULL STACK DEVELOPER</span>

            <h1>
              Meet
              <br />
              <span>Snehal.</span>
            </h1>

            <p className="hero-description">
              I build practical software and AI-powered applications using
              modern web technologies.
            </p>

            <div className="tech-line">
              Java
              <span>•</span>
              React
              <span>•</span>
              Node.js
              <span>•</span>
              Spring Boot
              <span>•</span>
              AI
            </div>

            <div className="hero-actions">
              <button
                className="primary-button"
                onClick={() => setActiveView("ai")}
              >
                <MessageCircle size={18} />
                Talk to Snehal AI
                <ArrowUpRight size={17} />
              </button>

              <button
                className="secondary-button"
                onClick={() =>
                  document
                    .getElementById("projects")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                View Work
                <ChevronRight size={17} />
              </button>
            </div>
          </div>

          {/* AI Representative card */}

          <div className="ai-card">
            <div className="ai-card-header">
              <div className="ai-identity">
                <div className="ai-icon">
                  <Sparkles size={20} />
                </div>

                <div>
                  <strong>SNEHAL AI</strong>
                  <span>Candidate Representative</span>
                </div>
              </div>

              <div className="online-status">
                <span></span>
                ONLINE
              </div>
            </div>

            <div className="ai-card-body">
              <h2>
                Don't just view
                <br />
                my portfolio.
                <br />
                <span>Ask it.</span>
              </h2>

              <p>
                Explore my technical background, projects, experience and career
                profile through my AI representative.
              </p>
            </div>

            <button
              className="ai-card-button"
              onClick={() => setActiveView("ai")}
            >
              Ask Snehal AI
              <ArrowUpRight size={17} />
            </button>
          </div>
        </section>

        {/* ================= SNAPSHOT ================= */}

        <section className="snapshot-section">
          <div className="section-heading">
            <div>
              <span className="section-label">QUICK VIEW</span>
              <h2>Candidate Snapshot</h2>
            </div>
          </div>

          <div className="snapshot-card">
            <div className="candidate-info">
              <div className="candidate-avatar">SB</div>

              <div>
                <h3>Snehal Krushna Bandal</h3>

                <p>Full Stack Developer · IT Undergraduate</p>

                <div className="location">
                  <MapPin size={14} />
                  Mumbai, Maharashtra · Open to relocation
                </div>
              </div>
            </div>

            <div className="stats">
              <div className="stat">
                <strong>9.13</strong>
                <span>CGPA</span>
              </div>

              <div className="stat">
                <strong>5+</strong>
                <span>PROJECTS</span>
              </div>

              <div className="stat">
                <strong>4</strong>
                <span>INTERNSHIPS</span>
              </div>

              <div className="stat">
                <strong>2027</strong>
                <span>GRADUATION</span>
              </div>
            </div>
          </div>
        </section>

        {/* ================= PROFILE DETAILS ================= */}

        <section className="profile-details-section">
          {/* SKILLS */}
          <div className="profile-detail-block" id="skills">
            <div className="section-heading">
              <div>
                <span className="section-label">TECHNICAL PROFILE</span>
                <h2>Skills</h2>
              </div>
            </div>

            <div className="skills-list">
              <span>Java</span>
              <span>HTML</span>
              <span>CSS</span>
              <span>JavaScript</span>
              <span>React.js</span>
              <span>Node.js</span>
              <span>Express.js</span>
              <span>Spring Boot</span>
              <span>SQL</span>
              <span>MySQL</span>
              <span>MongoDB</span>
              <span>REST APIs</span>
            </div>
          </div>

          {/* EXPERIENCE */}
          <div className="profile-detail-block" id="experience">
            <div className="section-heading">
              <div>
                <span className="section-label">PROFESSIONAL BACKGROUND</span>
                <h2>Experience</h2>
              </div>
            </div>

            <div className="experience-list">
              <div className="experience-item">
                <div>
                  <h3>EduSkills Foundation</h3>
                  <p>Java Full Stack Developer Intern</p>
                </div>
                <span>Apr 2026 – Jul 2026</span>
              </div>

              <div className="experience-item">
                <div>
                  <h3>AICTE</h3>
                  <p>Data Analyst Intern</p>
                </div>
                <span>Feb 2026 – Mar 2026</span>
              </div>

              <div className="experience-item">
                <div>
                  <h3>Edunet Foundation</h3>
                  <p>Full Stack Web Development Intern</p>
                </div>
                <span>Aug 2025 – Oct 2025</span>
              </div>

              <div className="experience-item">
                <div>
                  <h3>VaultofCodes</h3>
                  <p>Web Development Intern</p>
                </div>
                <span>Aug 2025 – Sep 2025</span>
              </div>
            </div>
          </div>

          {/* EDUCATION */}
          <div className="profile-detail-block" id="education">
            <div className="section-heading">
              <div>
                <span className="section-label">ACADEMIC BACKGROUND</span>
                <h2>Education</h2>
              </div>
            </div>

            <div className="education-list">
              <div className="education-item">
                <div>
                  <h3>B.E. Information Technology</h3>
                  <p>Atharva College of Engineering, Mumbai</p>
                </div>
                <strong>2027</strong>
              </div>

              <div className="education-item">
                <div>
                  <h3>Diploma in Information Technology</h3>
                  <p>Government Polytechnic Awasari (KH)</p>
                </div>
                <strong>2024</strong>
              </div>

              <div className="education-item">
                <div>
                  <h3>Secondary School Certificate (SSC)</h3>
                  <p>93.40%</p>
                </div>
                <strong>2020</strong>
              </div>
            </div>
          </div>
        </section>

        {/* ================= PROJECT PREVIEW ================= */}

        <section className="projects-section" id="projects">
          <div className="section-heading">
            <div>
              <span className="section-label">SELECTED WORK</span>
              <h2>Project Lab</h2>
            </div>

            <button
              className="text-button"
              onClick={() => setShowAllProjects((previous) => !previous)}
            >
              {showAllProjects ? "Show less" : "View all"}
              <ArrowUpRight size={15} />
            </button>
          </div>

          <div className="project-grid">
            {/* PROJECT 01 — FITNESS */}
            <article className="project-card">
              <div className="project-number">01</div>

              <span className="project-category">MICROSERVICES · AI</span>

              <h3>AI Fitness Tracking</h3>

              <p>
                AI-powered fitness recommendation system built with a scalable
                backend architecture.
              </p>

              <div className="project-tech">
                Spring Boot · React · Microservices
              </div>

              <div className="project-actions">
                <button
                  className="project-link"
                  onClick={() =>
                    openProjectInAI(
                      "Tell me about the AI-Powered Fitness Tracking System.",
                    )
                  }
                >
                  Explore project
                  <ArrowUpRight size={14} />
                </button>

                <a
                  className="project-github"
                  href="https://github.com/SnehalKrushnaBandal/fitness-microservices"
                  target="_blank"
                  rel="noreferrer"
                >
                  GitHub
                  <ArrowUpRight size={14} />
                </a>
              </div>
            </article>

            {/* PROJECT 02 — LEGALLENS */}
            <article className="project-card">
              <div className="project-number">02</div>

              <span className="project-category">AI · FULL STACK</span>

              <h3>LegalLens</h3>

              <p>
                AI-assisted packaged commodity inspection and Legal Metrology
                compliance platform.
              </p>

              <div className="project-tech">
                React · FastAPI · Gemini · OCR · YOLO
              </div>

              <div className="project-actions">
                <button
                  className="project-link"
                  onClick={() => openProjectInAI("Tell me about LegalLens.")}
                >
                  Explore project
                  <ArrowUpRight size={14} />
                </button>

                <a
                  className="project-github"
                  href="https://github.com/SnehalKrushnaBandal/LegalLens"
                  target="_blank"
                  rel="noreferrer"
                >
                  GitHub
                  <ArrowUpRight size={14} />
                </a>
              </div>
            </article>

            {/* PROJECT 03 — AI RESUME SCREENING */}
            <article className="project-card">
              <div className="project-number">03</div>

              <span className="project-category">AI · RECRUITMENT</span>

              <h3>AI Resume Screening</h3>

              <p>
                AI-powered application for analyzing resumes against job
                requirements.
              </p>

              <div className="project-tech">
                Python · LLM · Prompt Engineering
              </div>

              <div className="project-actions">
                <button
                  className="project-link"
                  onClick={() =>
                    openProjectInAI(
                      "Tell me about the AI Resume Screening System.",
                    )
                  }
                >
                  Explore project
                  <ArrowUpRight size={14} />
                </button>

                <a
                  className="project-github"
                  href="https://github.com/SnehalKrushnaBandal/AI-Resume-Screening-System"
                  target="_blank"
                  rel="noreferrer"
                >
                  GitHub
                  <ArrowUpRight size={14} />
                </a>
              </div>
            </article>

            {/* PROJECT 04 — CAFE MANAGEMENT */}
            {showAllProjects && (
              <article className="project-card">
                <div className="project-number">04</div>

                <span className="project-category">FULL STACK · WEB</span>

                <h3>Cafe Management System</h3>

                <p>
                  A web-based application designed to manage cafe operations and
                  streamline day-to-day activities.
                </p>

                <div className="project-tech">Java · MySQL · HTML · CSS</div>

                <div className="project-actions">
                  <button
                    className="project-link"
                    onClick={() =>
                      openProjectInAI(
                        "Tell me about the Cafe Management System.",
                      )
                    }
                  >
                    Explore project
                    <ArrowUpRight size={14} />
                  </button>

                  <a
                    className="project-github"
                    href="https://github.com/SnehalKrushnaBandal/Cafe-Management-System"
                    target="_blank"
                    rel="noreferrer"
                  >
                    GitHub
                    <ArrowUpRight size={14} />
                  </a>
                </div>
              </article>
            )}

            {/* PROJECT 05 — STEGOAI */}
            {showAllProjects && (
              <article className="project-card">
                <div className="project-number">05</div>

                <span className="project-category">AI · SECURITY</span>

                <h3>StegoAI</h3>

                <p>
                  An AI-assisted application focused on secure information
                  handling and intelligent analysis.
                </p>

                <div className="project-tech">Python · AI · FastAPI</div>

                <div className="project-actions">
                  <button
                    className="project-link"
                    onClick={() => openProjectInAI("Tell me about StegoAI.")}
                  >
                    Explore project
                    <ArrowUpRight size={14} />
                  </button>

                  <a
                    className="project-github"
                    href="https://github.com/SnehalKrushnaBandal"
                    target="_blank"
                    rel="noreferrer"
                  >
                    GitHub
                    <ArrowUpRight size={14} />
                  </a>
                </div>
              </article>
            )}
          </div>
        </section>

        {/* ================= RECRUITER MODE ================= */}

        <section className="recruiter-section">
          <div className="recruiter-card">
            <div className="recruiter-icon">
              <Bot size={23} />
            </div>

            <span className="section-label">FOR RECRUITERS</span>

            <h2>Have a job description?</h2>

            <p>
              Let Snehal AI analyze the role against the candidate profile and
              explain the relevant skills and experience.
            </p>

            <button
              className="primary-button"
              onClick={() => setActiveView("ai")}
            >
              Analyze a Job Description
              <ArrowUpRight size={17} />
            </button>
          </div>
        </section>

        {/* ================= FOOTER ================= */}

        <footer className="footer">
          <div>
            <strong>SNEHAL.AI</strong>
            <span>AI-Powered Developer Representative</span>
          </div>

          <div className="footer-links">
            <a href="#">GitHub</a>
            <a href="#">LinkedIn</a>
            <a href="#">Resume</a>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
