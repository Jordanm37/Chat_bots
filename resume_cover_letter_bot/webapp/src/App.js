import React, { useState } from "react";

function App() {
  const [resume, setResume] = useState(null);
  const [jobLink, setJobLink] = useState("");
  const [personalDetails, setPersonalDetails] = useState("");
  const [extraInstructions, setExtraInstructions] = useState("");
  const [loadingSection1, setLoadingSection1] = useState(false);
  const [loadingSection2, setLoadingSection2] = useState(false);
  const [section1Done, setSection1Done] = useState(false);
  const [downloadLink, setDownloadLink] = useState(null);

  const handleResumeUpload = (e) => {
    setResume(e.target.files[0]);
  };

  const handleSetClick = async () => {
    setLoadingSection1(true);
    const formData = new FormData();
    formData.append("resume_file", resume);
    formData.append("job_link", jobLink);
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/upload_resume_and_job_url/",
        {
          method: "POST",
          body: formData,
        }
      );
      const result = await response.json();
      if (result.status === "success") {
        setSection1Done(true);
      } else {
        alert("Failed to update resume and job link");
      }
    } catch (error) {
      alert("An error occurred: " + error.message);
    } finally {
      setLoadingSection1(false);
    }
  };

  const handleGenerateClick = async () => {
    setLoadingSection2(true);
    const data = {
      personal_details: personalDetails,
      extra_instructions: extraInstructions,
    };
    try {
      const response = await fetch("http://127.0.0.1:8000/generate_docx/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        setDownloadLink(url);
      } else {
        alert("Failed to generate DOCX file");
      }
    } catch (error) {
      alert("An error occurred: " + error.message);
    } finally {
      setLoadingSection2(false);
    }
  };

  const styles = {
    container: {
      background: "#000",
      color: "#fff",
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    },
    header: {
      fontSize: "48px",
      fontWeight: "bold",
      margin: "20px",
    },
    subheader: {
      // Add your subheader styles here
      fontSize: "1rem",
      fontWeight: "normal",
      marginTop: "0.5rem",
    },
    input: {
      background: "#222",
      border: "2px solid #555",
      borderRadius: "5px",
      color: "#fff",
      width: "300px",
      padding: "10px",
      margin: "10px",
    },
    logo: {
      position: "absolute",
      right: "20px",
      bottom: "20px",
      width: "100px",
    },
    section: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      marginBottom: "20px",
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>Cover Letter Generator</div>
      <div style={styles.subheader}>
        1. Upload your resume and paste the job link
      </div>
      <div style={styles.subheader}>
        2. Enter your Name and any extra instructions, eg "Add ___ detail about
        __" "Write in ___ tone" or "Use ____ keywords" ect
      </div>
      <div style={styles.subheader}>
        3. Click generate and download your new resume. It may take up to 3
        minutes for the magic to happen.
      </div>
      <div style={styles.section}>
        <input
          type="file"
          accept=".docx"
          onChange={handleResumeUpload}
          style={styles.input}
        />
        {resume && <div>Selected file: {resume.name}</div>}
        <input
          type="text"
          placeholder="Job link"
          value={jobLink}
          onChange={(e) => setJobLink(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleSetClick} style={styles.input}>
          {loadingSection1 ? "Loading..." : section1Done ? "Done" : "Set"}
        </button>
      </div>
      <div style={styles.section}>
        <textarea
          placeholder="Personal details"
          value={personalDetails}
          onChange={(e) => setPersonalDetails(e.target.value)}
          style={styles.input}
        />
        <textarea
          placeholder="Extra instructions"
          value={extraInstructions}
          onChange={(e) => setExtraInstructions(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleGenerateClick} style={styles.input}>
          {loadingSection2 ? "Loading..." : "Generate"}
        </button>
        {downloadLink && (
          <a
            href={downloadLink}
            download="output.docx"
            style={{ color: "#fff" }}
          >
            Click here to download
          </a>
        )}
      </div>
      <img src="/logo.png" alt="Logo" style={styles.logo} />
    </div>
  );
}
export default App;

// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
