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

const nerColors = {
  OPE: "red",
  PAY: "turquoise",
  LIN: "orange",
  NET: "yellow",
  SER: "darkgreen",
  APP: "maroon",
  ORG: "bordeaux",
  PER: "pink",
  LOC: "brown",
  NUM: "purple",
  DATE: "indigo",
  PKG: "lightgreen",
  OTH: "blue",
  BANK: "black"
}

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
      .post("http://127.0.0.1:5000/api/analyze", { text })
      .then((response) => {
        const analysis = response.data.analysis;
        const sentiment = response.data.sentiment;
  
        if (analysis === "sentiment") {
          if (sentiment === "Negative") {
            setResult(language === "ENG" ? "Negative" : "Negatif");
            setResultColor("red");
          } else if (sentiment === "Neutral") {
            setResult(language === "ENG" ? "Neutral" : "Nötr");
            setResultColor("yellow");
          } else if (sentiment === "Positive") {
            setResult(language === "ENG" ? "Positive" : "Pozitif");
            setResultColor("green");
          }
        } 
        else if (analysis === "ner") {
          const nerButtons = response.data.ner.map((item, index) => (
            <button
              key={index}
              className="ner-button"
              style={{ backgroundColor: nerColors[item.label] || "gray" }} // Default to gray if no match
            >
              {item.label}: {item.text}
            </button>
          ));
          setResult(nerButtons); // Store buttons in state
          setResultColor(""); // Reset color for NER results
        } 
        else if (analysis === "both") {
          const nerButtons = response.data.ner.map((item, index) => (
            <button
              key={index}
              className="ner-button"
              style={{ backgroundColor: nerColors[item.label] || "gray" }} // Default to gray if no match
            >
              {item.label}: {item.text}
            </button>
          ));
          setResult(nerButtons); // Store buttons in state
          setResultColor(""); // Reset color for NER results
        } 
        else {
          console.log("No Analysis");
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
