from db import db
from flask import session, request, abort
import users

def send(message, thread_id, user_id):  # thread_id and topic_id to be included w/message? 
    user_id = users.user_id()
    if user_id == 0:
        return False

    if session["csrf_token"] != request.form["csrf_token"]:    # to take into acc. CSRF-vulnerability
        abort(403)

    sql = "INSERT INTO allmessages (content, thread_id, user_id, sent_at) VALUES (:content, :thread_id, :user_id, NOW())"
    db.session.execute(sql, {"content":message, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True   

def new_thread(topic_id, user_id, thread): #9.4
    sql="INSERT INTO threads (topic_id, user_id, thread) VALUES (:topic_id, :user_id, :thread) RETURNING id"
    result=db.session.execute(sql, {"topic_id": topic_id, "user_id":user_id, "thread":thread})
    db.session.commit()
    return result.fetchone()


def get_list():
    #sql = "SELECT topics.topic FROM topics"
    sql="SELECT topics.id, topics.topic FROM topics"   #add topics.id to get threads correctly
    result = db.session.execute(sql)
    return result.fetchall()


def get_threads(topic_id):  #7.4
    print("haetaan threadit")
    user_id=users.user_id()  # additional: take into acc if admin or not???
    sql="SELECT threads.id, threads.thread, allusers.username FROM threads, allusers "\
        "WHERE threads.topic_id=:topic_id AND allusers.id=threads.user_id "\
        "ORDER BY threads.id DESC"
    result=db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id})  #admin?
    return result.fetchall()    


def get_messages(thread_id): #8.4
    sql="SELECT allusers.username, allmessages.sent_at, allmessages.content, allmessages.id "\
        "FROM allusers, allmessages WHERE allmessages.thread_id=:thread_id "\
        "AND allusers.id=allmessages.user_id "\
        "ORDER BY allmessages.id"  
    result=db.session.execute(sql, {"thread_id": thread_id, "user_id": users.user_id()})   
    return result.fetchall()       


def get_path(topic_id, thread_id): #8.4
    sql="SELECT topics.topic, threads.thread FROM topics, threads "\
        "WHERE topics.id=:topic_id AND threads.id=:thread_id"     
    result=db.session.execute(sql, {"topic_id":topic_id, "thread_id":thread_id})
    return result.fetchone()      

    
def get_topic_name(topic_id):   #7.4
    print("haetaan topic name")
    sql="SELECT topic FROM topics WHERE id=:topic_id"
    result =db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()[0]
