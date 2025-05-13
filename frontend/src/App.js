import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [fileNames, setFileNames] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [isUploading, setIsUploading] = useState(false);


  const handleUpload = async () => {
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }
  
    try {
      setIsUploading(true); // 👉 Start loader
      await axios.post("http://localhost:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(`${files.length} PDF(s) uploaded and indexed.`);
    } catch (err) {
      console.error("Upload Error:", err);
      alert("Upload failed: " + err.message);
    } finally {
      setIsUploading(false); // 👉 Stop loader
    }
  };
  

  const handleAsk = async () => {
    const formData = new FormData();
    formData.append("question", question);

    const newMessages = [...messages, { sender: "user", text: question }];
    setMessages(newMessages);
    setQuestion("");

    try {
      const res = await axios.post("http://localhost:8000/ask/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessages([...newMessages, { sender: "bot", text: res.data.answer }]);
      setChatHistory(prev => [
        ...prev,
        {
          id: Date.now(),
          timestamp: new Date().toLocaleString(),
          messages: [...newMessages, { sender: "bot", text: res.data.answer }]
        }
      ]);
    } catch (err) {
      console.error("Ask Error:", err);
      alert("Ask failed: " + err.message);
    }
  };

  return (
    <div className="app-wrapper">
      <div className="sidebar">
        <h2>Chat History</h2>
        {chatHistory.length === 0 ? (
          <p className="empty-history">No chats yet</p>
        ) : (
          chatHistory.map((chat) => (
            <div
              key={chat.id}
              className="history-item"
              onClick={() => setMessages(chat.messages)}
            >
              <span>{chat.timestamp}</span>
            </div>
          ))
        )}
      </div>

      <div className="chat-container">
        <h1 className="title">PDF ChatBot</h1>

        <div className="upload-bar">
          <label className="file-label">
            📎 Choose PDF(s)
            <input
              type="file"
              multiple
              accept="application/pdf"
              onChange={(e) => {
                setFiles(e.target.files);
                setFileNames(Array.from(e.target.files).map(f => f.name));
              }}
            />
          </label>
          {fileNames.length > 0 && (
            <div className="file-info">
              {fileNames.length === 1
                ? fileNames[0]
                : `${fileNames.length} PDFs selected`}
            </div>
          )}
          <button className="upload-btn" onClick={handleUpload}>
            Upload
          </button>
          {isUploading && <p className="upload-loader">Processing PDF(s)...</p>}
        </div>


        <div className="chat-box">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`bubble-wrapper ${msg.sender === "user" ? "right" : "left"}`}
            >
              <div className={`chat-bubble ${msg.sender}`}>
                {msg.text}
              </div>
            </div>
          ))}
          {messages.length === 0 && (
            <p className="empty-chat">Start a conversation by uploading a PDF and asking a question.</p>
          )}


        </div>

        <div className="input-area">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
          />
          <button onClick={handleAsk} disabled={question.trim() === ""}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
