import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingAnswer, setLoadingAnswer] = useState(false);

  // URL du backend Flask
  const BACKEND_URL = "http://127.0.0.1:5050";

  const uploadPDF = async () => {
    if (!file) return alert("Choisis un fichier PDF à uploader");
    setLoadingUpload(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      alert(data.message || data.error);
    } catch (error) {
      alert("Erreur upload : " + error.message);
    }

    setLoadingUpload(false);
  };

  const askQuestion = async () => {
    if (!question.trim()) return alert("Pose une question");
    setLoadingAnswer(true);

    try {
      const res = await fetch(`${BACKEND_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setAnswer(data.response || data.error);
    } catch (error) {
      setAnswer("Erreur : " + error.message);
    }

    setLoadingAnswer(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>SmartPDF Chatbot</h1>

      <section>
        <h2>Uploader un PDF</h2>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          disabled={loadingUpload}
        />
        <button onClick={uploadPDF} disabled={loadingUpload} style={{ marginLeft: 10 }}>
          {loadingUpload ? "Upload en cours..." : "Uploader"}
        </button>
      </section>

      <hr style={{ margin: "30px 0" }} />

      <section>
        <h2>Poser une question</h2>
        <textarea
          rows={4}
          style={{ width: "100%" }}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Tape ta question ici..."
          disabled={loadingAnswer}
        />
        <button onClick={askQuestion} disabled={loadingAnswer || !question.trim()} style={{ marginTop: 10 }}>
          {loadingAnswer ? "En cours..." : "Envoyer"}
        </button>

        <div
          style={{
            marginTop: 20,
            minHeight: 100,
            whiteSpace: "pre-wrap",
            backgroundColor: "#f0f0f0",
            padding: 10,
            borderRadius: 5,
            border: "1px solid #ccc",
          }}
        >
          {answer || "La réponse s’affichera ici..."}
        </div>
      </section>
    </div>
  );
}

export default App;
