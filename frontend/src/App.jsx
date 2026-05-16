import { useState } from "react";
import axios from "axios";

function App() {

  const [file, setFile] = useState(null);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  // Upload PDF
  const uploadPDF = async () => {

    if (!file) {
      alert("Please upload a PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      setLoading(true);

      await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      alert("PDF uploaded successfully");

    } catch (error) {

      console.error(error);

      alert("Upload failed");

    } finally {

      setLoading(false);

    }

  };

  // Ask Question
  const askQuestion = async () => {

    if (!question) return;

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/ask",
        {
          question
        }
      );

      setAnswer(response.data.answer);

    } catch (error) {

      console.error(error);

      alert("Failed to get answer");

    } finally {

      setLoading(false);

    }

  };

  return (

    <div style={styles.container}>

      <h1>AI College Q&A Chatbot</h1>

      {/* Upload Section */}
      <div style={styles.card}>

        <h2>Upload PDF</h2>

        <input
          type="file"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
        />

        <button onClick={uploadPDF}>
          Upload PDF
        </button>

      </div>

      {/* Chat Section */}
      <div style={styles.card}>

        <h2>Ask Questions</h2>

        <textarea
          rows="4"
          placeholder="Ask something from the PDF..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
        />

        <button onClick={askQuestion}>
          Ask AI
        </button>

      </div>

      {/* Answer Section */}
      {loading && (
        <p>Thinking...</p>
      )}

      {answer && (

        <div style={styles.answerBox}>

          <h3>AI Response</h3>

          <p>{answer}</p>

        </div>

      )}

    </div>

  );

}

const styles = {

  container: {
    width: "70%",
    margin: "40px auto",
    fontFamily: "Arial"
  },

  card: {
    background: "white",
    padding: "20px",
    borderRadius: "10px",
    marginBottom: "20px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
  },

  answerBox: {
    background: "#f8fafc",
    padding: "20px",
    borderRadius: "10px",
    border: "1px solid #ccc"
  }

};

export default App;