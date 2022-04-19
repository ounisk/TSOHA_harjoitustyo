from sqlalchemy import true
from app import app
from flask import render_template, redirect, request, session, abort
import users, messages


@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", topics=list)    # add: no. of threads, no. of messages and time of last msg


@app.route("/topic/<int:topic_id>")  # 7.4
def topic(topic_id):
    list = messages.get_threads(topic_id)
    name = messages.get_topic_name(topic_id)
    return render_template("topic.html", threads=list, topic_id=topic_id, topic_name=name)


@app.route("/topic/<int:topic_id>/thread/<int:thread_id>")
def thread(topic_id, thread_id):
    list = messages.get_messages(thread_id)
    path = messages.get_path(topic_id, thread_id)
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

        if len(username) < 1:
            return render_template("error.html", message="Käyttäjätunnus liian lyhyt")
        if len(username) > 50:
            return render_template("error.html", message="Käyttäjätunnus liian pitkä")    
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if len(password1) < 1:
            return render_template("error.html", message="Salasana liian lyhyt")
        if password1 != password2:
            return render_template("error.html", message="Salasana ei täsmää")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut, valitse toinen käyttäjätunnus")



@app.route("/create_new_topic") #11.4, 
def create_new_topic():
    return render_template("new_topic_template.html")


@app.route("/new_topic", methods=["POST"])   #11.4, 12.4
def new_topic():

    if not session.get("admin", 0):   #if not admin, can't create new topics
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)

    topic_name = request.form["topic_name"]
    visible = request.form.get("visible")
    #print("visibility", visibility)

    if len(topic_name) < 1 or len(topic_name) > 100:
        return render_template("error.html", message="Aiheen tulee olla 1-100 merkkiä")

    #print("mitä on visiblessa?", visible)
    messages.new_topic(topic_name, visible)
    return redirect("/")


@app.route("/access/<int:topic_id>")    #13.4
def access(topic_id):
    return render_template("access.html", topic_id=topic_id)


@app.route("/grant_topic_access", methods=["POST"])    #13.4
def grant_topic_access():
    if not session.get("admin", 0):   #if not admin, can't give access
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)

    topic_id = request.form["topic_id"]
    #print("topic_id", topic_id)
    username=request.form["username"]

    if len(username) < 1 or len(username) > 50:
            return render_template("error.html", message="Käyttäjätunnuksen pituus on 1-50 merkkiä")
       
    user_id = users.get_user_id(username)

    if not user_id:
        return render_template("error.html", message=str(username) + " ei ole tietokannassa")

    users.grant_access(topic_id, user_id)
    return redirect("/")


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
    topic_id = request.form["topic_id"]

    if len(thread_name) < 1 or len(thread_name) > 100:
        return render_template("error.html", message="Keskustelun otsikon tulee olla 1-100 merkkiä.")

    if len(first_message) < 1 or len(first_message) > 5000:
        return render_template("error.html", message="Viestin pituus pitää olla 1-5000 merkkiä.")

    thread_id = messages.new_thread(topic_id, user_id, thread_name)[0]
    messages.send(first_message, thread_id, user_id)

    return redirect("/topic/" + str(topic_id))




@app.route("/edit_thread/<int:topic_id>/<int:thread_id>")   #18.4
def edit_thread(topic_id, thread_id):
    return render_template("edit_thread.html", topic_id=topic_id, thread_id=thread_id)


@app.route("/edit_thread_header", methods=["POST"])    #18.4
def edit_thread_header():
    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)
    thread_name = request.form["thread_name"]  
    thread_id = request.form["thread_id"]  
    topic_id = request.form["topic_id"]

    if len(thread_name) < 1 or len(thread_name) > 100:
        return render_template("error.html", message="Keskustelun otsikon tulee olla 1-100 merkkiä.")

    messages.edit_thread(thread_id, thread_name)

    return redirect("/topic/" + str(topic_id))


@app.route("/delete_thread/<int:thread_id>", methods=["GET"])   #18.4
def delete_thread(thread_id):
    #if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
    #    abort(403)   #not working???
    #thread_id = request.form["thread_id"]    
    topic_id = messages.delete_this_thread(thread_id)[0]

    return redirect("/topic/" + str(topic_id))



@app.route("/message/<int:topic_id>/<int:thread_id>")   
def message(topic_id, thread_id):     #fixed 9.4,
    return render_template("message.html", topic_id=topic_id, thread_id=thread_id)   #  add topic 4.4 


@app.route("/new_message", methods=["POST"])   # modified 9.4
def new_message():
    #check if signed-in???
    user_id = users.user_id()

    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)

    message = request.form["message"]   
    topic_id = request.form["topic_id"]   
    thread_id = request.form["thread_id"]    

    if len(message) > 5000:
        return render_template("error.html", message="Viesti on liian pitkä.") #

    if len(message) < 1:
        return render_template("error.html", message="Viesti on liian lyhyt.") #    
   
    if messages.send(message, thread_id, user_id):
        #return redirect("/")   # or return redirect("/topic"+ topic_id)  ??
        return redirect("/topic/" + str(topic_id) + "/thread/" + str(thread_id))
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut.")




@app.route("/edit_message/<int:topic_id>/<int:thread_id>/<int:message_id>")   #19.4
def edit_message(topic_id, thread_id, message_id): # include old content
    return render_template("edit_message.html", topic_id=topic_id, thread_id=thread_id, message_id=message_id)


@app.route("/edit_message_text", methods=["POST"])   #19.4
def edit_message_text():
    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)
    message = request.form["message"]  
    topic_id = request.form["topic_id"]   
    thread_id = request.form["thread_id"] 
    message_id = request.form["message_id"]  

    if len(message) > 5000:
        return render_template("error.html", message="Viesti on liian pitkä.") #

    if len(message) < 1:
        return render_template("error.html", message="Viesti on liian lyhyt.") # 

    messages.edit_message(message, message_id)
    return redirect("/topic/" + str(topic_id) + "/thread/" + str(thread_id))


@app.route("/delete_message/<int:topic_id>/<int:thread_id>/<int:message_id>", methods=["GET"])   #19.4
def delete_message(topic_id, thread_id, message_id):
    #if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
    #    abort(403)   #not working???
    #thread_id = request.form["thread_id"]    
    thread_id = messages.delete_this_message(message_id)[0]

    return redirect("/topic/" + str(topic_id) + "/thread/" + str(thread_id))


@app.route("/search")    #16.4
def search():
    return render_template("search.html")

@app.route("/search_result", methods=["GET"])    #16.4
def search_result():
    query = request.args["query"]
    if len(query) < 1 or len(query) > 50:
        return render_template("error.html", message = "Haettavan sanan pituus voi olla 1-50 merkkiä.")
    result_messages = messages.search_message(query)
    #print("result_messages", result_messages)
    if result_messages is None or len(result_messages) == 0:
        return render_template("error.html", message = "Hakusanalla ei löydy viestejä.")

    return render_template("search_result.html", messages = result_messages)
