from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def user_home():
    """home page"""

    return render_template("survey_start.html")

@app.post("/begin")
def start_button():
    """start button that will redirect the page to a question page"""
    session["responses"] = []

    flash("please fill out the answer")
    return redirect(f"/question/0")


@app.post("/answer")
def answer():
    """answer for the question"""
    answer = request.form.get('answer')

    #update the session with the answer
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses


    print(f"\n\n\ncurrent response: {responses}\n\n\n")

    if len(survey.questions) == len(responses):
        flash("Thank you")
        return redirect("/end_page")
    else:
        flash("please fill out the answer")
        return redirect(f"/question/{len(responses)}")

@app.get("/question/<int:question_num>")
def question_0(question_num):
    """get question 0"""

    responses = session['responses']

    if question_num == len(responses):
        question = survey.questions[question_num]
        return render_template("question.html",question = question )
    else:
        flash('please complete the survey in order')
        return redirect(f"/question/{len(responses)}")




@app.get("/end_page")
def end_page():
    responses = session['responses']
    questions = survey.questions

    return render_template("completion.html", questions=questions, response=responses)














