from app import app
from flask import render_template, redirect, request, session, abort
import users, messages


@app.route("/")
def index():
    list=messages.get_list()
    return render_template("index.html", topics=list)    # add: no. of threads, no. of messages and time of last msg


@app.route("/topic/<int:topic_id>")  # 7.4
def topic(topic_id):
    print("topic_id", topic_id)
    list=messages.get_threads(topic_id)
    name=messages.get_topic_name(topic_id)
    return render_template("topic.html", threads=list, topic_id=topic_id, topic_name=name)


@app.route("/topic/<int:topic_id>/thread/<int:thread_id>")
def thread(topic_id,thread_id):
    list=messages.get_messages(thread_id)
    path=messages.get_path(topic_id, thread_id)
    return render_template("thread.html", messages=list, topic_id=topic_id, thread_id=thread_id, message_path=path)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            #print("printtausta jos löytyy")
            return redirect("/")
        else:
            #print("printtaus jos ei löydy login")
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


@app.route("/new_thread_template/<int:topic_id>")   #9.4
def new(topic_id):
    return render_template("new_thread_template.html", topic_id=topic_id)


@app.route("/new_thread", methods=["POST"])   #9.4
def new_thread():
    user_id = users.user_id()

    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)

    thread_name = request.form["thread_name"]   
    first_message = request.form["message"] 
    topic_id=request.form["topic_id"]

    if len(thread_name) < 1 or len(thread_name) > 100:
        return render_template("error.html", message="Keskustelun otsikon tulee olla 4-100 merkkiä")

    if len(first_message) < 1 or len(first_message) > 5000:
        return render_template("error.html", message="Viestin pituus pitää olla 1-5000 merkkiä")

    thread_id = messages.new_thread(topic_id, user_id, thread_name)[0]
    messages.send(first_message, thread_id, user_id)

    return redirect("/topic/" + str(topic_id))


@app.route("/message/<int:id>")    # vai <text:topic> vai ota pois? ei ole vielä gitissä
def message(id):     #lisätty topic 4.4, vai (topic)
    return render_template("message.html", id=id)   # lisätty topic 4.4 vai topic=topic


@app.route("/new_message", methods=["POST"])   # modified 9.4
def new_message():
    #check if signed-in???
    user_id = users.user_id()

    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)

    message = request.form["message"]   #message.html
    topic_id=request.form("topic_id")   #here?
    thread_id=request.form("thread_id")    #here?

    if len(message) > 5000:
        return render_template("error.html", message="Viesti on liian pitkä") #

    if messages.send(message, thread_id, user_id):
        return redirect("/")   # or return redirect("/topic"+ topic_id)  ??
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")
