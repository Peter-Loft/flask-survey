from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """Generates landing page"""
    session["responses"] = []
    return render_template("survey_start.html", survey=survey)


@app.get("/question/<int:questionnum>")
def questionpage(questionnum):
    """Route for questions after first one"""
    if len(session["responses"]) == len(survey.questions):
        return redirect("/completion")

    if questionnum >= len(survey.questions):
        return redirect(f"/question/{len(session['responses'])}")

    if questionnum != len(session["responses"]):
        return redirect(f"/question/{len(session['responses'])}")

    else:
        question = survey.questions[questionnum]
        return render_template("question.html", question=question)


@app.post("/begin")
def first_question():
    """Route for first question"""

    question = survey.questions[0]

    return render_template("question.html", question=question)


@app.post("/answer")
def answer():
    """Saves answer user submitted and redirect to next question or 
    completed page"""
    responses = session["responses"]
    responses.append(request.form.get("answer"))
    session["responses"] = responses
    if len(responses) < len(survey.questions):
        return redirect(f"/question/{len(responses)}")
    else:
        return redirect("/completion")


@app.get("/completion")
def completion():
    """Generates completion page"""
    return render_template("completion.html")
