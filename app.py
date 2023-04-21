from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

response = []

@app.get("/")
def user_home():
    """home page"""

    return render_template("survey_start.html")

@app.post("/begin")
def start_button():
    """start button that will redirect the page to a question page"""

    flash("please fill out the answer")
    return redirect("/question/0")

@app.get("/question/<int:question_num>")
def question_0(question_num):
    """get question 0"""

    question = survey.questions[question_num]
    # print(survey.questions)

    return render_template("question.html",question = question )

@app.post("/answer")
def answer():
    """answer for the question"""
    global response
    # put answer in responses
    answer = request.form.get('answer')
    response.append(answer)


    print(f"\n\n\ncurrent response: {response}\n\n\n")

    if len(survey.questions) == len(response):


        saved_response = response[::1]
        response = []

        flash("Thank you")
        return redirect("/end_page")
    else:
        flash("please fill out the answer")
        return redirect(f"/question/{len(response)}")


        # end page ->

@app.get("/end_page")
def end_page():

    return render_template("completion.html")














