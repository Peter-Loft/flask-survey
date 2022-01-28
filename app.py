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
    # CR might want to move the intialization of the responses list
    session["responses"] = []
    return render_template("survey_start.html", survey=survey)


@app.get("/question/<int:questionnum>")
def questionpage(questionnum):
    """Route for questions after first one
    If user tries to access wrong question, it will redirect back to
    proper question or completion with warning flash"""

    # CR maybe differentiate the flash messages

    if len(session["responses"]) == len(survey.questions):
        flash("You've already finished the survey")
        return redirect("/completion")

    if questionnum >= len(survey.questions):
        flash("You are trying to access wrong question")
        return redirect(f"/question/{len(session['responses'])}")

    if questionnum != len(session["responses"]):
        flash("You are trying to access wrong question")
        return redirect(f"/question/{len(session['responses'])}")

    else:
        question = survey.questions[questionnum]
        return render_template("question.html", question=question)


@app.post("/begin")
def first_question():
    """Route for first question"""
    # CR maybe move session initialization here
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
