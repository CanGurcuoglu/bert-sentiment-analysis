import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const translations = {
  ENG: {
    title: "BERT Sentiment Analysis",
    selectedLanguage: "Language",
    analyze: "Analyze",
    predictionResult: "My Prediction:",
    enterText: "Enter text here...",
  },
  TR: {
    title: "BERT Duygu Analizi",
    selectedLanguage: "Dil",
    analyze: "Analiz",
    predictionResult: "Tahminim:",
    enterText: "Buraya yazın...",
  },
};

const App = () => {
  const [language, setLanguage] = useState("ENG");
  const [text, setText] = useState("");
  const [result, setResult] = useState(null); // Store result as null initially
  const [resultColor, setResultColor] = useState(""); // Store color of result container

  // Change Language with Toggle
  const toggleLanguage = () => {
    const newLanguage = language === "ENG" ? "TR" : "ENG";
    setText(""); // Clear the text input
    setResult(""); // Clear the prediction result
    setResultColor(""); // Reset the result color
    axios
      .post("http://127.0.0.1:5000/api/language", { language: newLanguage })
      .then(() => {
        setLanguage(newLanguage);
      })
      .catch((error) => console.error(error));
  };

  // Predict Sentiment
  const predictSentiment = () => {
    axios
      .post("http://127.0.0.1:5000/api/predict", { text })
      .then((response) => {
        const prediction = response.data.result;
        setResult(prediction);
        
        // Set the color based on the result
        if (prediction === 0) {
          setResultColor("red");
        } else if (prediction === 1) {
          setResultColor("yellow");
        } else if (prediction === 2) {
          setResultColor("green");
        }
      })
      .catch((error) => console.error(error));
  };

  const t = translations[language]; // Select translations based on the current language

  return (
    <div className="app-container">
      <h1 className="app-title">{t.title}</h1>
      <div className="toggle-container">
        <label className="toggle-label">
          <input
            type="checkbox"
            checked={language === "ENG"}
            onChange={toggleLanguage}
            className="toggle-input"
          />
          <span className="toggle-slider"></span>
        </label>
        <p className="language-info">
          {t.selectedLanguage}: {language === "ENG" ? "English" : "Türkçe"}
        </p>
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder={t.enterText}
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="text-input"
        />
        <button className="btn" onClick={predictSentiment}>
          {t.analyze}
        </button>
      </div>
      <div
        className={`result-container ${resultColor}`} // Apply the dynamic color class
      >
        <h2 className="result-title">{t.predictionResult}</h2>
        <p className="result-text">{result !== null ? result : ""}</p>
      </div>
    </div>
  );
};

export default App;
