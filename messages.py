from db import db
import users

def send(message, thread_id):  # thread_id and topic_id to be included w/message? 
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO allmessages (content, thread_id, user_id, sent_at) VALUES (:content, :thread_id, :user_id, NOW())"
    db.session.execute(sql, {"content":message, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True    

def get_list():
    sql = "SELECT topics.topic FROM topics"
    result = db.session.execute(sql)
    return result.fetchall()
