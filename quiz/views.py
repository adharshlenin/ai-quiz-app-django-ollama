import json
import re
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

OLLAMA_URL = "http://127.0.0.1:11434"

@csrf_exempt
def index(request):
    quiz_data = None
    error = None
    score = None
    total = 0
    user_answers = None

    # Load quiz from session if available
    session_quiz = request.session.get("quiz_data")

    if request.method == "POST":
        # -------------------------------
        # CASE 1: User Submits Answers
        # -------------------------------
        if "submit_answers" in request.POST:
            if not session_quiz:
                error = "Session expired or no quiz found. Please generate a quiz first."
            else:
                quiz_data = session_quiz
                total = len(quiz_data)
                user_answers = []
                score = 0

                # Collect user answers and calculate score
                for i in range(total):
                    ans = request.POST.get(f"answer_{i}")
                    user_answers.append(ans)

                    if ans == quiz_data[i].get("answer"):
                        score += 1

                return render(request, "quiz/result.html", {
                    "quiz_data": quiz_data,
                    "score": score,
                    "total": total,
                    "user_answers": user_answers,
                })

        # -------------------------------
        # CASE 2: User Generates New Quiz
        # -------------------------------
        else:
            topic = request.POST.get("topic", "").strip()
            if not topic:
                error = "Please enter a topic to generate a quiz."
            else:
                prompt = (
                    f"You are an API. Return only a JSON array. "
                    f"Generate a 5-question multiple-choice quiz on the topic '{topic}'. "
                    "Each question should be an object with: 'question', 'options' (with keys A-D), and 'answer' (one of A-D). "
                    "Respond ONLY with JSON. Example: "
                    "[{\"question\": \"What is Python?\", \"options\": {\"A\": \"Snake\", \"B\": \"Programming Language\", \"C\": \"Car\", \"D\": \"Movie\"}, \"answer\": \"B\"}]"
                )

                try:
                    payload = {
                        "model": "llama2:7b",
                        "prompt": prompt,
                        "stream": False
                    }
                    headers = {"Content-Type": "application/json"}

                    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, headers=headers)
                    response.raise_for_status()

                    data = response.json()
                    raw_quiz = data.get("response", "")
                    print("OLLAMA RAW:", raw_quiz)

                    # Extract and clean the JSON quiz data
                    cleaned_quiz = re.sub(r"```json|```", "", raw_quiz, flags=re.IGNORECASE).strip()
                    match = re.search(r"\[.*\]", cleaned_quiz, re.DOTALL)

                    if match:
                        cleaned_quiz = match.group(0)
                        quiz_data = json.loads(cleaned_quiz)

                        if isinstance(quiz_data, list):
                            request.session["quiz_data"] = quiz_data
                            total = len(quiz_data)
                        else:
                            error = "Invalid quiz format received."
                            quiz_data = None
                    else:
                        error = "Ollama did not return a valid JSON quiz array."

                except requests.exceptions.RequestException as e:
                    error = f"Error connecting to Ollama: {e}"
                except json.JSONDecodeError:
                    error = "Failed to parse Ollama's quiz output. Make sure it's valid JSON."

    else:
        # On GET, clear any previous quiz data
        request.session.pop("quiz_data", None)

    # Render main index page
    return render(request, "quiz/index.html", {
        "quiz_data": quiz_data,
        "error": error,
        "score": score,
        "total": total,
        "user_answers": user_answers,
    })
