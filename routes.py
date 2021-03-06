from sqlalchemy import true
from flask import render_template, redirect, request, session, abort
from app import app
import users, messages


@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", topics=list)

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    if users.has_access(topic_id) is None:
        return render_template("error.html", message="Käyttäjällä ei oikeutta sivuun")

    list = messages.get_threads(topic_id)
    name = messages.get_topic_name(topic_id)
    return render_template("topic.html", threads=list, topic_id=topic_id, topic_name=name)


@app.route("/topic/<int:topic_id>/thread/<int:thread_id>")
def thread(topic_id, thread_id):
    if users.has_access(topic_id) is None:
        return render_template("error.html", message="Käyttäjällä ei oikeutta sivuun")

    list = messages.get_messages(thread_id)
    path = messages.get_path(topic_id, thread_id)
    return render_template("thread.html", messages=list, topic_id=topic_id, thread_id=thread_id, message_path=path)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            error = "Käyttäjätunnus tai salasana on väärin."
            #return render_template("error.html", message="Käyttäjätunnus tai salasana on väärin")
            return render_template("login.html", error=error)


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

@app.route("/create_new_topic")
def create_new_topic():
    return render_template("new_topic_template.html")

@app.route("/new_topic", methods=["POST"])
def new_topic():

    if not session.get("admin", 0):
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    topic_name = request.form["topic_name"]
    visible = request.form.get("visible")

    if len(topic_name) < 1 or len(topic_name) > 100:
        return render_template("error.html", message="Aiheen tulee olla 1-100 merkkiä")

    messages.new_topic(topic_name, visible)
    return redirect("/")



@app.route("/hide_topic/<int:topic_id>", methods=["GET"])
def hide_topic(topic_id):
    if not session.get("admin", 0):
        abort(403)

    messages.hide_topic(topic_id)
    return redirect("/")


@app.route("/hide_secret_topic/<int:topic_id>", methods=["GET"])
def hide_secret_topic(topic_id):
    if not session.get("admin", 0):
        abort(403)

    messages.hide_secret_topic(topic_id)
    return redirect("/")


@app.route("/access/<int:topic_id>")
def access(topic_id):
    return render_template("access.html", topic_id=topic_id)


@app.route("/grant_topic_access", methods=["POST"])
def grant_topic_access():
    if not session.get("admin", 0):
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    topic_id = request.form["topic_id"]
    username = request.form["username"]

    if len(username) < 1 or len(username) > 50:
        return render_template("error.html", message="Käyttäjätunnuksen pituus on 1-50 merkkiä")

    user_id = users.get_user_id(username)

    if not user_id:
        return render_template("error.html", message=str(username) + " ei ole tietokannassa")

    users.grant_access(topic_id, user_id)
    return redirect("/")


@app.route("/new_thread_template/<int:topic_id>")
def new(topic_id):
    return render_template("new_thread_template.html", topic_id=topic_id)


@app.route("/new_thread", methods=["POST"])
def new_thread():
    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="Et ole kirjautunut sisään.")

    if session["csrf_token"] != request.form["csrf_token"]:
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


@app.route("/edit_thread/<int:topic_id>/<int:thread_id>")
def edit_thread(topic_id, thread_id):
    thread_name = messages.get_thread_to_edit(thread_id)
    return render_template("edit_thread.html", topic_id=topic_id, thread_id=thread_id, thread_name=thread_name)


@app.route("/edit_thread_header", methods=["POST"])
def edit_thread_header():
    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="Et ole kirjautunut sisään.")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    thread_name = request.form["thread_name"]
    thread_id = request.form["thread_id"]
    topic_id = request.form["topic_id"]

    if users.thread_edit_access(thread_id) is None:
        return render_template("error.html", message="Käyttäjällä ei oikeutta muokata ketjua.")

    if len(thread_name) < 1 or len(thread_name) > 100:
        return render_template("error.html", message="Keskustelun otsikon tulee olla 1-100 merkkiä.")

    messages.edit_thread(thread_id, thread_name)

    return redirect("/topic/" + str(topic_id))


@app.route("/delete_thread/<int:thread_id>", methods=["GET"])
def delete_thread(thread_id):
    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="Et ole kirjautunut sisään.")

    if users.thread_edit_access(thread_id) is None:
        return render_template("error.html", message="Käyttäjällä ei oikeutta muokata ketjua.")

    topic_id = messages.delete_this_thread(thread_id)[0]

    return redirect("/topic/" + str(topic_id))



@app.route("/message/<int:topic_id>/<int:thread_id>")
def message(topic_id, thread_id):
    return render_template("message.html", topic_id=topic_id, thread_id=thread_id)


@app.route("/new_message", methods=["POST"])
def new_message():
    error = None

    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="Et ole kirjautunut sisään.")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    message = request.form["message"]
    topic_id = request.form["topic_id"]
    thread_id = request.form["thread_id"]

    if len(message) > 5000:
        error = "Viesti on liian pitkä."
        return render_template("message.html", error=error, topic_id=topic_id, thread_id=thread_id) # 4.5 että toimii virheessä oikein

    if len(message) < 1:
        error = "Viesti on liian lyhyt."
        return render_template("message.html", error=error, topic_id=topic_id, thread_id=thread_id) # 4.5

    if messages.send(message, thread_id, user_id):
        return redirect("/topic/" + str(topic_id) + "/thread/" + str(thread_id))
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut.")


@app.route("/edit_message/<int:topic_id>/<int:thread_id>/<int:message_id>")
def edit_message(topic_id, thread_id, message_id):
    message = messages.get_message_to_edit(message_id)
    return render_template("edit_message.html", topic_id=topic_id, thread_id=thread_id, message_id=message_id, message=message)


@app.route("/edit_message_text", methods=["POST"])
def edit_message_text():
    user_id = users.user_id()

    error = None

    if user_id == 0:
        return render_template("error.html", message="Et ole kirjautunut sisään.")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    message = request.form["message"]
    topic_id = request.form["topic_id"]
    thread_id = request.form["thread_id"]
    message_id = request.form["message_id"]

    if users.message_edit_access(message_id) is None:
        return render_template("error.html", message="Käyttäjällä ei oikeutta muokata viestiä.")

    if len(message) > 5000:
        error = "Viesti on liian pitkä."
        return render_template("edit_message.html", error=error, topic_id=topic_id, thread_id=thread_id, message_id=message_id, message=message)
        #return render_template("error.html", message="Viesti on liian pitkä.")

    if len(message) < 1:
        error = "Viesti on liian lyhyt."
        return render_template("edit_message.html", error=error, topic_id=topic_id, thread_id=thread_id, message_id=message_id, message=message)
        #return render_template("error.html", message="Viesti on liian lyhyt.")

    messages.edit_message(message, message_id)
    return redirect("/topic/" + str(topic_id) + "/thread/" + str(thread_id))


@app.route("/delete_message/<int:topic_id>/<int:thread_id>/<int:message_id>", methods=["GET"])   #19.4
def delete_message(topic_id, thread_id, message_id):

    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="Et ole kirjautunut sisään.")

    if users.message_edit_access(message_id) is None:
        return render_template("error.html", message="Käyttäjällä ei oikeutta poistaa viestiä.")

    thread_id = messages.delete_this_message(message_id)[0]

    return redirect("/topic/" + str(topic_id) + "/thread/" + str(thread_id))


@app.route("/search")
def search():
    user_id = users.user_id()
    if user_id == 0:
        return render_template("error.html", message="Voit hakea viestejä, kun olet kirjautunut sisään.")
    return render_template("search.html")

@app.route("/search_result", methods=["GET"])
def search_result():
    query = request.args["query"]
    if len(query) < 1 or len(query) > 50:
        return render_template("error.html", message="Haettavan sanan pituus voi olla 1-50 merkkiä.")
    result_messages = messages.search_message(query)

    if result_messages is None or len(result_messages) == 0:
        return render_template("error.html", message="Hakusanalla ei löydy viestejä.")

    return render_template("search_result.html", messages=result_messages)
