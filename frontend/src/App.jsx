import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const translations = {
  ENG: {
    title: "HAVELSAN AI",
    selectedLanguage: "Language",
    analyze: "Analyze",
    predictionResult: "My Prediction:",
    enterText: "Enter text here...",
    welcomeMessage: "Hello, Welcome to HAVELSAN AI Service! I can help you with sentiment anlaysis, ner analysis or both analysis. Please enter your sentence."
  },
  TR: {
    title: "HAVELSAN AI",
    selectedLanguage: "Dil",
    analyze: "Analiz",
    predictionResult: "Tahminim:",
    enterText: "Buraya yazın...",
    welcomeMessage: "Merhaba, HAVELSAN AI hizmetine hoşgeldiniz! Size duygu analizi, adlandırılmış varlık analizi veya her ikisinde de  yardımcı olabilirim. Lütfen cümlenizi girin."
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
  const [messages, setMessages] = useState([]); // Stores chat messages

  useEffect(() => {
    setMessages([{ text: translations[language].welcomeMessage, type: "bot" }]);
  }, []);

  const toggleLanguage = () => {
    const newLanguage = language === "ENG" ? "TR" : "ENG";
    setText("");
    setResult(null);
    setResultColor("");
    setNerButtons([]);
    setMessages([{text: translations[newLanguage].welcomeMessage, type: "bot"}]);
    axios
      .post("http://127.0.0.1:5000/api/language", { language: newLanguage })
      .then(() => setLanguage(newLanguage))
      .catch((error) => console.error(error));
  };

  const deleteText = () => {
    setText("");
  }

  const predictSentiment = () => {
    if (!text.trim()) return;

    axios
      .post("http://127.0.0.1:5000/api/analyze", { text })
      .then((response) => {
        console.log(response.data);
        const { analysis, sentiment, ner, chat } = response.data;

        let newResult = null;
        let newColor = "";
        let newNerButtons = [];

        if (analysis === "sentiment") {
          if (sentiment === "Negative") {
            newResult = language === "ENG" ? "Negative" : "Negatif";
          } else if (sentiment === "Neutral") {
            newResult = language === "ENG" ? "Neutral" : "Nötr";
          } else if (sentiment === "Positive") {
            newResult = language === "ENG" ? "Positive" : "Pozitif";
          }
          console.log(newResult);
          setMessages((prevMessages) => [
            ...prevMessages,
            { text, type: "user" },
            { text: newResult, type: "bot" },
          ]);
          setText(""); // Clear input field
        }

        if (analysis === "ner") {
          newNerButtons = ner.map((item, index) => (
            <button
              key={index}
              className="ner-button"
              style={{ backgroundColor: nerColors[item.label] || "gray" }}
            >
              {item.label}: {item.text}
            </button>
          ));
          setMessages((prevMessages) => [
            ...prevMessages,
            { text, type: "user" },
            { text: newNerButtons, type: "bot" },
          ]);
          setText(""); // Clear input field
          
        }

        if(analysis === "both") {
          if (sentiment === "Negative") {
            newResult = language === "ENG" ? "Negative" : "Negatif";
          } else if (sentiment === "Neutral") {
            newResult = language === "ENG" ? "Neutral" : "Nötr";
          } else if (sentiment === "Positive") {
            newResult = language === "ENG" ? "Positive" : "Pozitif";
          }
          console.log(newResult);
          newNerButtons = ner.map((item, index) => (
            <button
              key={index}
              className="ner-button"
              style={{ backgroundColor: nerColors[item.label] || "gray" }}
            >
              {item.label}: {item.text}
            </button>
          ));
          
          setMessages((prevMessages) => [
            ...prevMessages,
            { text, type: "user" },
            { text: newResult, type: "bot" },
            { text: newNerButtons, type: "bot" },

          ]);
          setText(""); // Clear input field

        }

        if (analysis === "else") {
          setMessages((prevMessages) => [
            ...prevMessages,
            { text, type: "user" },
            { text: chat, type: "bot" },
          ]);
          setText(""); // Clear input field
        } else {
          setResult(newResult);
          setResultColor(newColor);
          setNerButtons(newNerButtons);
        }
      })
      .catch((error) => console.error(error));
  };

  const t = translations[language];

  return (
    <div className="app-container">
      <h1 className="app-title">{t.title}</h1>
      {/* Chat Display */}
      <div className="chat-container">
        {messages.map((msg, index) => (
            <div key={index} className="message-wrapper" style={{ justifyContent: msg.type === "user" ? "flex-end" : "flex-start" }}>
              
              <div className={`chat-message ${msg.type === "user" ? "user-msg" : "bot-msg"}`}>
                {msg.text}
              </div>
            </div>
            ))}
      </div>
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
          <button className="btn-del" onClick={deleteText}>  
            
            {t.analyze ? (  
                <svg width="16px" height="16px" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
                  <path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z" fill="white"/></svg> 
              ) : (  
                <svg xmlns="http://www.w3.org/2000/svg">  
                  <path d="M498.1 5.6c10.1 7 15.4 19.1 13.5 31.2l-64 416c-1.5 9.7-7.4 18.2-16 23s-18.9 5.4-28 1.6L284 427.7l-68.5 74.1c-8.9 9.7-22.9 12.9-35.2 8.1S160 493.2 160 480l0-83.6c0-4 1.5-7.8 4.2-10.8L331.8 202.8c5.8-6.3 5.6-16-.4-22s-15.7-6.4-22-.7L106 360.8 17.7 316.6C7.1 311.3 .3 300.7 0 288.9s5.9-22.8 16.1-28.7l448-256c10.7-6.1 23.9-5.5 34 1.4z" fill="red"/>  
        
                </svg>  
              )}  
          </button>
      </div>
    </div>
  );
};

export default App;