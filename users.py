import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db



def login(username, password):
    #sql = "SELECT id, password FROM allusers WHERE username=:username"   # select also admin?? comm. su 3.4.2022
    sql = "SELECT id, password, admin FROM allusers WHERE username=:username" #corrected 11.4 with admin
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["admin"] = user.admin  #added 11.4
            session["csrf_token"] = secrets.token_hex(16) #CSRF, see: part 4, insert into the form as well?
            return True
        else:
            return False

def logout():
    #del session["username"] del 24.4
    del session["user_id"]
    del session["admin"]  #added 11.4
    del session["csrf_token"]  #added 24.4


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO allusers (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False    # if username in use, error
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def is_admin():   #14.4
    return session.get("admin", 0)

def get_user_id(username):   #13.4
    sql = "SELECT id FROM allusers WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        return user.id
    else:
        return False

def grant_access(topic_id, user_id): #13.4
    sql = "INSERT INTO topics_private (topic_id, user_id) VALUES (:topic_id, :user_id)"
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    db.session.commit()

def has_access(topic_id):   #22.4 - unauthorized can't access secret pages
    user_id = session.get("user_id", 0)
    is_admin = session.get("admin", 0)
    if is_admin == 0:
        is_admin = False
    sql = "SELECT topics.id FROM topics WHERE topics.id=:topic_id "\
        "AND (topics.visible=TRUE OR :is_admin OR :user_id IN "\
        "(SELECT topics_private.user_id FROM topics_private "\
        "WHERE topics_private.topic_id=topics.id))"
    result = db.session.execute(sql, {"topic_id":topic_id, "is_admin":is_admin, "user_id":user_id})
    return result.fetchone()

def thread_edit_access(thread_id):   #23.4 - unauthorized can't access secret pages
    user_id = session.get("user_id", 0)
    is_admin = session.get("admin", 0)
    if is_admin == 0:
        is_admin = False
    sql = "SELECT id FROM threads WHERE id=:thread_id "\
        "AND (user_id=:user_id OR :is_admin)"
    result = db.session.execute(sql, {"thread_id":thread_id, "is_admin":is_admin, "user_id":user_id})
    return result.fetchone()

def message_edit_access(message_id):   #23.4 - unauthorized can't access secret pages
    user_id = session.get("user_id", 0)
    is_admin = session.get("admin", 0)
    if is_admin == 0:
        is_admin = False
    sql = "SELECT id FROM allmessages WHERE id=:message_id "\
        "AND (user_id=:user_id OR :is_admin)"
    result = db.session.execute(sql, {"message_id":message_id, "is_admin":is_admin, "user_id":user_id})
    return result.fetchone()
