from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def homepage():

    return render_template("survey_start.html", survey=survey)

@app.get("/question/<int:questionnum>")
def questionpage(questionnum):

    question = survey.questions[questionnum]


    return render_template("question.html", question=question, choices = question.choices)

@app.post("/begin")
def first_question():

    question = survey.questions[0]

    return render_template("question.html", questionnum = 0, question=question, choices = question.choices)

@app.post("/answer")
def answer():

    responses.append(request.form.get("answer"))

    if len(responses) < len(survey.questions):
        return redirect(f"/question/{len(responses)}")
    else:
        return redirect("/completion")

@app.get("/completion")
def completion():
    return render_template("completion.html")