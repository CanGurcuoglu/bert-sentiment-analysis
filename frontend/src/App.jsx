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
  NET: "#b8af09",
  SER: "darkgreen",
  APP: "maroon",
  ORG: "bordeaux",
  PER: "pink",
  LOC: "brown",
  NUM: "purple",
  DATE: "indigo",
  PKG: "lightgreen",
  OTH: "blue",
  BANK: "black",
};

const App = () => {
  const [language, setLanguage] = useState("ENG");
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [resultColor, setResultColor] = useState("");
  const [nerButtons, setNerButtons] = useState([]);

  const toggleLanguage = () => {
    const newLanguage = language === "ENG" ? "TR" : "ENG";
    setText("");
    setResult(null);
    setResultColor("");
    setNerButtons([]);
    axios
      .post("http://127.0.0.1:5000/api/language", { language: newLanguage })
      .then(() => setLanguage(newLanguage))
      .catch((error) => console.error(error));
  };

  const predictSentiment = () => {
    axios
      .post("http://127.0.0.1:5000/api/analyze", { text })
      .then((response) => {
        const { analysis, sentiment, ner } = response.data;

        let newResult = null;
        let newColor = "";
        let newNerButtons = [];

        console.log(analysis);

        if (analysis === "sentiment" || analysis === "both") {
          if (sentiment === "Negative") {
            newResult = language === "ENG" ? "Negative" : "Negatif";
            newColor = "red";
          } else if (sentiment === "Neutral") {
            newResult = language === "ENG" ? "Neutral" : "Nötr";
            newColor = "yellow";
          } else if (sentiment === "Positive") {
            newResult = language === "ENG" ? "Positive" : "Pozitif";
            newColor = "green";
          }
        }

        if (analysis === "ner" || analysis === "both") {
          newNerButtons = ner.map((item, index) => (
            <button
              key={index}
              className="ner-button"
              style={{ backgroundColor: nerColors[item.label] || "gray" }}
            >
              {item.label}: {item.text}
            </button>
          ));
        }

        if(analysis !== "sentiment" && analysis !== "ner") {
          console.log("Zortingen Strasse")
        }

        setResult(newResult);
        setResultColor(newColor);
        setNerButtons(newNerButtons);
      })
      .catch((error) => console.error(error));
  };

  const t = translations[language];

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
          
        {t.analyze ? (
            <svg width="16px" height="16px" viewBox="0 0 512 512"  xmlns="http://www.w3.org/2000/svg">
              <path d="M498.1 5.6c10.1 7 15.4 19.1 13.5 31.2l-64 416c-1.5 9.7-7.4 18.2-16 23s-18.9 5.4-28 1.6L284 427.7l-68.5 74.1c-8.9 9.7-22.9 12.9-35.2 8.1S160 493.2 160 480l0-83.6c0-4 1.5-7.8 4.2-10.8L331.8 202.8c5.8-6.3 5.6-16-.4-22s-15.7-6.4-22-.7L106 360.8 17.7 316.6C7.1 311.3 .3 300.7 0 288.9s5.9-22.8 16.1-28.7l448-256c10.7-6.1 23.9-5.5 34 1.4z" fill="white"/>
  
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg">
              <path d="M498.1 5.6c10.1 7 15.4 19.1 13.5 31.2l-64 416c-1.5 9.7-7.4 18.2-16 23s-18.9 5.4-28 1.6L284 427.7l-68.5 74.1c-8.9 9.7-22.9 12.9-35.2 8.1S160 493.2 160 480l0-83.6c0-4 1.5-7.8 4.2-10.8L331.8 202.8c5.8-6.3 5.6-16-.4-22s-15.7-6.4-22-.7L106 360.8 17.7 316.6C7.1 311.3 .3 300.7 0 288.9s5.9-22.8 16.1-28.7l448-256c10.7-6.1 23.9-5.5 34 1.4z" fill="red"/>
  
            </svg>
          )}
        </button>
      </div>
      <div className="results-wrapper">
  {nerButtons.length > 0 && result ? (
    <>
      <div className="result-container">{nerButtons}</div>
      <div className={`result-container-copy ${resultColor}`}>
        <p className="result-text">{result}</p>
      </div>
    </>
  ) : (
    <>
      {nerButtons.length > 0 && (
        <div className="result-container">{nerButtons}</div>
      )}
      {result && (
        <div className={`result-container-copy ${resultColor}`}>
          <p className="result-text">{result}</p>
        </div>
      )}
    </>
  )}
</div>
    </div>
  );
};

export default App;