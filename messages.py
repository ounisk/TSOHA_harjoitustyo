from flask import session, request, abort
from db import db
import users

def send(message, thread_id, user_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    sql = "INSERT INTO allmessages (content, thread_id, user_id, sent_at) "\
        "VALUES (:content, :thread_id, :user_id, NOW())"
    db.session.execute(sql, {"content":message, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True


def get_message_to_edit(message_id):
    sql = "SELECT allmessages.content FROM allmessages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return result.fetchone()[0]


def edit_message(content, message_id):
    sql = "UPDATE allmessages SET content=:content WHERE id=:message_id"
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()


def delete_this_message(message_id):
    sql = "DELETE FROM allmessages WHERE id=:message_id RETURNING thread_id"
    result = db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return result.fetchone()


def new_thread(topic_id, user_id, thread):
    sql = "INSERT INTO threads (topic_id, user_id, thread) VALUES "\
        "(:topic_id, :user_id, :thread) RETURNING id"
    result = db.session.execute(sql, {"topic_id": topic_id, "user_id":user_id, "thread":thread})
    db.session.commit()
    return result.fetchone()


def get_thread_to_edit(thread_id):
    sql = "SELECT threads.thread FROM threads WHERE id=:thread_id"
    result = db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
    return result.fetchone()[0]


def edit_thread(thread_id, thread):
    sql = "UPDATE threads SET thread=:thread WHERE id=:thread_id"
    db.session.execute(sql, {"thread":thread, "thread_id": thread_id})
    db.session.commit()


def delete_this_thread(thread_id):
    sql = "DELETE FROM threads WHERE id=:thread_id RETURNING topic_id"
    result = db.session.execute(sql, {"thread_id": thread_id})
    db.session.commit()
    return result.fetchone()



def new_topic(topic, visible):
    sql = "INSERT INTO topics (topic, visible) VALUES (:topic, :visible)"
    db.session.execute(sql, {"topic":topic, "visible":visible})
    db.session.commit()
    return True


def hide_topic(topic_id):
    sql = "UPDATE topics SET visible=FALSE, topic='**PIILOTETTU** ' || topic WHERE id=:topic_id"
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()


def hide_secret_topic(topic_id):
    sql = "DELETE FROM topics_private WHERE topic_id=:topic_id"
    sql2 = "UPDATE topics SET topic='**PIILOTETTU** ' || topic WHERE id=:topic_id"
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.execute(sql2, {"topic_id":topic_id})
    db.session.commit()


def get_list():
    user_id = users.user_id()

    is_admin = users.is_admin()
    if is_admin == 0:
        is_admin = False
    sql = "SELECT topics.id, topics.topic, Totalcounter.Threadcounter, "\
        "Totalcounter.Messagescounter, Totalcounter.Time, topics.visible "\
        "FROM topics "\
        "LEFT JOIN (SELECT threads.topic_id, COUNT(threads.id) Threadcounter, "\
        "SUM(Threadmessages.Messagecounter) Messagescounter, MAX(Threadmessages.time) Time FROM threads "\
        "JOIN (SELECT allmessages.thread_id, COUNT(allmessages.id) Messagecounter, MAX(allmessages.sent_at) Time "\
        "FROM allmessages "\
        "GROUP BY allmessages.thread_id) Threadmessages ON Threadmessages.thread_id=threads.id "\
        "GROUP BY threads.topic_id) Totalcounter ON Totalcounter.topic_id=topics.id "\
        "WHERE topics.visible=TRUE OR :is_admin OR :user_id IN "\
        "(SELECT topics_private.user_id FROM topics_private WHERE topics_private.topic_id=topics.id) "\
        "ORDER BY topics.visible DESC, topics.id"
    result = db.session.execute(sql, {"is_admin":is_admin, "user_id":user_id})
    return result.fetchall()


def get_threads(topic_id):
    user_id = users.user_id()
    is_admin = users.is_admin()
    if is_admin == 0:
        is_admin = False
    sql = "SELECT threads.id, threads.thread, allusers.username, (SELECT COUNT(allmessages.id) "\
        "FROM allmessages WHERE threads.id=allmessages.thread_id), (threads.user_id=:user_id OR :is_admin=TRUE) "\
        "FROM threads, allusers "\
        "WHERE threads.topic_id=:topic_id AND allusers.id=threads.user_id "\
        "ORDER BY threads.id DESC"
    result = db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id, "is_admin":is_admin})
    return result.fetchall()


def get_messages(thread_id):
    user_id = users.user_id()
    is_admin = users.is_admin()
    if is_admin == 0:
        is_admin = False
    sql = "SELECT allusers.username, allmessages.sent_at, allmessages.content, allmessages.id, "\
        "(allmessages.user_id=:user_id OR :is_admin=TRUE) "\
        "FROM allusers, allmessages WHERE allmessages.thread_id=:thread_id "\
        "AND allusers.id=allmessages.user_id "\
        "ORDER BY allmessages.id"
    result = db.session.execute(sql, {"thread_id": thread_id, "user_id": users.user_id(), "is_admin":is_admin})
    return result.fetchall()


def get_path(topic_id, thread_id):
    sql = "SELECT topics.topic, threads.thread FROM topics, threads "\
        "WHERE topics.id=:topic_id AND threads.id=:thread_id"
    result = db.session.execute(sql, {"topic_id":topic_id, "thread_id":thread_id})
    return result.fetchone()


def get_topic_name(topic_id):
    sql = "SELECT topic FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()[0]


def search_message(query):
    user_id = users.user_id()
    is_admin = users.is_admin()
    sql = " SELECT * FROM (SELECT topics.id, topics.topic, threads.id, threads.thread, allmessages.id, "\
        "allmessages.content, allmessages.sent_at "\
        "FROM allmessages JOIN threads ON allmessages.thread_id=threads.id  "\
        "JOIN topics ON threads.topic_id=topics.id "\
        "WHERE (topics.visible=TRUE OR :is_admin OR "\
        ":user_id IN (SELECT topics_private.user_id FROM topics_private "\
        "WHERE topics_private.topic_id=topics.id)) "\
        "ORDER BY allmessages.sent_at) results "\
        "WHERE LOWER(results.content) LIKE :query"

    result = db.session.execute(sql, {"query":"%"+query.lower()+"%", "user_id":user_id, "is_admin":is_admin})
    return result.fetchall()