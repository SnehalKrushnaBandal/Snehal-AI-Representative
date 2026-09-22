import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ArrowLeft, ArrowUp, Bot, Sparkles } from "lucide-react";
import { useEffect, useRef, useState } from "react";

function AIChat({ onBack, initialQuestion = "" }) {
  const initialQuestionSent = useRef(false);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const hasInitialQuestion = Boolean(initialQuestion);

  const askAI = async (questionText) => {
    const trimmedQuestion = questionText.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    setQuestion("");

    const userMessage = {
      role: "user",
      content: trimmedQuestion,
    };

    const assistantMessage = {
      role: "assistant",
      content: "",
    };

    const conversationHistory = messages;

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
      assistantMessage,
    ]);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
          history: conversationHistory,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to connect to Snehal AI");
      }

      if (!response.body) {
        throw new Error("Streaming is not supported by the response");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantAnswer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });

        assistantAnswer += chunk;

        setMessages((previousMessages) => {
          const updatedMessages = [...previousMessages];

          updatedMessages[updatedMessages.length - 1] = {
            role: "assistant",
            content: assistantAnswer,
          };

          return updatedMessages;
        });
      }
    } catch (error) {
      console.error(error);

      setMessages((previousMessages) => {
        const updatedMessages = [...previousMessages];

        updatedMessages[updatedMessages.length - 1] = {
          role: "assistant",
          content:
            "I couldn't connect to Snehal AI. Please make sure the backend is running.",
        };

        return updatedMessages;
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (
      initialQuestion &&
      messages.length === 0 &&
      !initialQuestionSent.current
    ) {
      initialQuestionSent.current = true;
      askAI(initialQuestion);
    }
  }, [initialQuestion]);

  const handleSubmit = (event) => {
    event.preventDefault();

    askAI(question);
  };

  const suggestedQuestions = [
    "What are Snehal's strongest technical skills?",
    "Which project demonstrates his backend skills?",
    "Tell me about Snehal's internship experience.",
    "Why did Snehal choose software development?",
  ];

  return (
    <div className="ai-chat-page">
      {/* Header */}

      <header className="ai-chat-header">
        <button className="back-button" onClick={onBack}>
          <ArrowLeft size={17} />
          Back
        </button>

        <div className="ai-chat-title">
          <div className="ai-chat-logo">
            <Sparkles size={17} />
          </div>

          <div>
            <strong>SNEHAL AI</strong>
            <span>Candidate Representative</span>
          </div>
        </div>

        <div className="chat-online">
          <span></span>
          ONLINE
        </div>
      </header>

      {/* Chat area */}

      <main className="chat-container">
        {messages.length === 0 ? (
          <div className="chat-welcome">
            <div className="large-ai-icon">
              <Bot size={27} />
            </div>

            <span className="section-label">AI REPRESENTATIVE</span>

            <h1>
              Ask anything
              <br />
              about Snehal.
            </h1>

            <p>
              Explore Snehal's technical background, projects, experience and
              career profile — or ask a question directly.
            </p>

            <div className="suggested-questions">
              {suggestedQuestions.map((question) => (
                <button
                  key={question}
                  className="suggestion-chip"
                  onClick={() => askAI(question)}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="messages-container">
            {messages.map((message, index) => (
              <div key={index} className={`message-row ${message.role}`}>
                {message.role === "assistant" && (
                  <div className="message-ai-icon">
                    <Sparkles size={15} />
                  </div>
                )}

                <div className="message-content">
                  <span className="message-label">
                    {message.role === "user" ? "RECRUITER" : "SNEHAL AI"}
                  </span>

                  <div className="message-text">
                    {message.role === "assistant" ? (
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {message.content}
                      </ReactMarkdown>
                    ) : (
                      message.content
                    )}

                    {message.role === "assistant" &&
                      loading &&
                      index === messages.length - 1 && (
                        <span className="typing-cursor">▌</span>
                      )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Input */}

        <form className="chat-input-wrapper" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ask something about Snehal..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            disabled={loading}
          />

          <button
            type="submit"
            disabled={!question.trim() || loading}
            className="send-button"
          >
            <ArrowUp size={18} />
          </button>
        </form>

        <p className="chat-disclaimer">
          Snehal AI answers using the candidate's resume and profile
          information.
        </p>
      </main>
    </div>
  );
}

export default AIChat;
