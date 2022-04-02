from app import app
from flask import render_template, redirect, request, session
import users, messages


@app.route("/")
def index():
    list=messages.get_list()
    return render_template("index.html", topics=list)    # add: no. of threads, no. of messages and time of last msg


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Käyttäjätunnus tai salasana on väärin")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")   


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]

        if len(username)<1:
            return render_template("error.html", message="Käyttäjätunnus liian lyhyt")
        if len(username)>50:
            return render_template("error.html", message="Käyttäjätunnus liian pitkä")    
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if len(password1)<1:
            return render_template("error.html", message="Salasana liian lyhyt")
        if password1 != password2:
            return render_template("error.html", message="Salasana ei täsmää")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut, valitse toinen käyttäjätunnus")



@app.route("/message")
def message():
    return render_template("message.html")


@app.route("/new_message", methods=["POST"])   # HUOM create message.html !!!!!!
def new_message():
    #check if signed-in???
    message = request.form["message"]   #message.html
    topic_id=request.form("topic_id")   #here?
    thread_id=request.form("thread_id")    #here?

    if len(message) > 5000:
        return render_template("error.html", message="Viesti on liian pitkä") #

    if messages.send(message, thread_id):
        return redirect("/")   # or return redirect("/topic"+ topic_id)  ??
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")
