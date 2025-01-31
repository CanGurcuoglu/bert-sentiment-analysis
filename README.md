# API KEY

api-key: 1c0b2cf7a9de4b2df64d4805e3293d61406d7fac                   # when using colab to train models

http://10.150.16.168:8080/user/signup/?token=reRp8covJe5yHozHr7wIGwpIRFpBWoor2JKfOZjI


# BERT SENTIMENT ANALYSIS

This project provides a web-based sentiment analysis tool built using BERT (Bidirectional Encoder Representations from Transformers). The tool supports both English and Turkish languages. The frontend is built with React, and the backend is built with Flask.

Prerequisites
Make sure you have the following installed on your machine:

Python (for the backend)
Node.js and npm (for the frontend)
Git (to clone the repository)


## Getting Started


1. Clone the Repository
  - First, clone the repository to your local machine.

```
git clone https://github.com/your-username/bert-sentiment-analysis.git
cd bert-sentiment-analysis
```


2. Set Up the Backend (Flask)
  - a. Navigate to the App directory.

```
cd App
```
  - b. Create a virtual environment.
It's recommended to use a virtual environment to manage the Python dependencies.

```
python -m venv venv
```
  - c. Activate the virtual environment.
For Windows:

```
.\venv\Scripts\activate
```
For Mac/Linux:

```
source venv/bin/activate
```
  - d. Install the backend dependencies.

```
pip install -r requirements.txt
```
  - e. Run the Flask backend.

```
python app.py
```
The Flask backend will start and listen for requests on http://127.0.0.1:5000.


3. Set Up the Frontend (React)
  - a. Navigate to the front/frontend directory.

```
cd front/frontend
```
  - b. Install the frontend dependencies.

```
npm install
```
  - c. Run the React development server.

```
npm start
```
The React frontend will start and be available at http://localhost:3000.


4. Open the App
Once both the backend and frontend servers are running, you can open your web browser and go to:

  - Frontend: http://localhost:3000
  - Backend: http://127.0.0.1:5000 (for API requests)
The frontend will interact with the Flask backend to analyze sentiment based on the text input.


5. Switching Between Languages
You can toggle between English and Turkish by clicking the language switcher on the frontend interface.


6. Stopping the Servers
To stop the servers:

Press Ctrl + C in the terminal where the React server is running.
Press Ctrl + C in the terminal where the Flask server is running.




