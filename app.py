from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def render_homepage():
    """renders home page + sets session for the user"""
    session["responses"] = []

    return render_template("survey_start.html")

@app.post("/begin")
def render_survey():
    """renders the first question of the survey"""

    flash("please fill out the answer")
    return redirect(f"/question/0")


@app.post("/answer")
def handle_answer_submission():
    """handles user submitting an answer to the survey question"""
    answer = request.form.get('answer')
    responses = session['responses']

    responses.append(answer)
    session['responses'] = responses


    if len(survey.questions) == len(responses):
        flash("Thank you")
        return redirect("/summary_page")
    else:
        flash("please fill out the answer")
        return redirect(f"/question/{len(responses)}")

@app.get("/question/<int:question_num>")
def render_question(question_num):
    """
    renders the appropriate question to the user, redirects them if they try
    to answer questions out of turn
    """

    responses = session['responses']

    if question_num == len(responses):
        question = survey.questions[question_num]
        return render_template("question.html",question = question )

    if len(survey.questions) == len(responses):
        flash('you have already completed the survey ')
        return redirect('/summary_page')

    else:
        flash('please complete the survey in order')
        return redirect(f"/question/{len(responses)}")


@app.get("/summary_page")
def render_summary_page():
    responses = session['responses']
    questions = survey.questions

    return render_template("completion.html", questions=questions, response=responses)














