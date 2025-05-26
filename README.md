# AI-Powered Quiz App (with Ollama)

## Overview

This is a dynamic AI-powered quiz web application built using Django and Ollama, a locally running large language model (LLM). The app lets users input any topic and generates multiple-choice quiz questions dynamically using AI, then evaluates the answers.

This project demonstrates:
- Integration of a local AI model for real-time quiz generation
- Handling form input, session management, and JSON data processing in Django
- Frontend rendering using Django templates
- Basic UI customization with a clean galaxy-themed design

## Tech Stack

- **Backend:** Django (Python)
- **AI Model:** Ollama (runs locally)
- **Frontend:** HTML, CSS (Galaxy-themed UI)
- **Database:** SQLite (default Django database)
- **Language:** Python
- **Deployment:** Localhost (can be extended to production)

## Features

- **Topic-Based Quiz Generation:**  
  Users enter any topic (e.g., "History of Computers"), which is sent to the local Ollama model. Ollama responds with quiz questions in JSON format.

- **Dynamic Question Rendering:**  
  The app dynamically displays questions and options using Django templates.

- **Answer Submission & Scoring:**  
  Users submit answers, and the app scores them with a detailed breakdown of correct and incorrect answers.

- **Galaxy-Themed UI:**  
  Clean and visually appealing user interface with static images and CSS styling.

## How Ollama is Used

- Ollama runs locally on your machine via command prompt.
- The Django backend sends prompts like:  
  `"Generate 5 multiple choice quiz questions on topic X in JSON format."`
- Ollama returns a JSON string containing questions, options, and correct answers.
- The app parses this JSON and renders it on the frontend.

### Example JSON format

```json
[
  {
    "question": "What is the capital of France?",
    "options": { "A": "Paris", "B": "London", "C": "Rome", "D": "Berlin" },
    "answer": "A"
  }
]
