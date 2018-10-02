#flask-taskr/db.pyimport psycopg2 as psy
import psycopg2 as psy
import psycopg2.extras as psyextra

CONNECTION_STRING = ''

def init(connection_string):
    global CONNECTION_STRING
    CONNECTION_STRING = connection_string    

def connectToDB():
    try:
        return psy.connect(CONNECTION_STRING)
    except:
        print("Can't connect to database!")    

def closeConnection(conn, cur = None):
    if cur != None:
        cur.close()
    conn.close()

def addNewUser(user):
    conn = connectToDB()
    cur = conn.cursor(cursor_factory = psy.extras.DictCursor)
    
    try:
        cur.execute("INSERT INTO dev.users (user_name, email, password, role) VALUES(%s, %s, %s, %s);",
                   (user.name, user.email, user.password, user.role))
    except Exception as e:
        conn.rollback()
        closeConnection(conn, cur)
        if int(e.pgcode) != 23505:
            print("Error code: {0}".format(e.pgcode))
            print(e)
            raise(e)           
        return False

    conn.commit()
    closeConnection(conn, cur)
    return True
    

def getUserCredentials(user, pwd):
    conn = connectToDB()
    cur = conn.cursor(cursor_factory = psy.extras.DictCursor)
    try:
        cur.execute("SELECT user_id, role, password FROM dev.users WHERE user_name = %s AND password = %s;", (user,pwd))
    except Exception as e:
        #raise e
        print(e)
        return None
    result = cur.fetchone()
    closeConnection(conn, cur)
    return result

#Task-related operations  

def getTaskInfo(taskID):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory = psy.extras.DictCursor)

  try:
    cur.execute("SELECT task_id, task_name, due_date, priority FROM dev.tasks WHERE task_id = %s;", (taskID,))
    #cur.execute('select name, due_date, priority, task_id from tasks where status=0')
  except Exception as e:
    #Log e
    raise(e) 

  result = cur.fetchone()

  cur.close()
  conn.close()

  return result


def getOpenTasks(user_id):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psy.extras.DictCursor)
  try:
    # TODO: Change dev.tasks to tasks in production 10/2/2018  
    cur.execute('select task_name, due_date, priority, task_id from dev.tasks where status=1 AND user_id=%s;',(user_id,))
  except Exception as e:
    print(e)
    raise(e)

  results = cur.fetchall()
  
  cur.close()
  conn.close()
  return results         

def getClosedTasks(user_id):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psy.extras.DictCursor)
  try:
    cur.execute('select task_name, due_date, priority, task_id from dev.tasks where status=0 AND user_id=%s;',(user_id,))
  except Exception as e:
    print(e)
    raise(e)

  results = cur.fetchall()
  
  cur.close()
  conn.close()
  return results     

def add_task(user_id, taskname, duedate, priority, status):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psy.extras.DictCursor)
  
  try:
    #cur.execute('select task_name, due_date, priority, task_id from tasks where status=0')
    cur.execute("INSERT INTO dev.tasks (user_id, task_name, due_date, priority, status) VALUES (%s, %s, %s, %s, %s);",
                (user_id, taskname, duedate, priority, 1))

  except Exception as e:
    print("INSERT INTO dev.tasks (user_id, task_name, due_date, priority, status) VALUES ({}, {}, {}, {}, {});".format(
          user_id, taskname, duedate, priority, status))
    print(e)
    conn.rollback()
    conn.close()
    raise(e)
    

  conn.commit()  
  cur.close()
  conn.close()
  

def update_task(task_id, taskname, duedate, priority):
  conn = connectToDB()
  cur = conn.cursor()

  try:
    cur.execute("UPDATE dev.tasks SET task_name=%s, due_date=%s, priority=%s WHERE task_id=%s;", 
                (taskname, duedate, priority, task_id))
  except Exception as e:
    print(e)
    raise(e) 

  conn.commit()
  cur.close()
  conn.close()

def update_task_complete(task_id, task_completed=False):
  conn = connectToDB()
  cur = conn.cursor()

  try:
    if task_completed == True:  
        cur.execute("UPDATE dev.tasks SET status = 0 WHERE task_id=%s;", (task_id,))
    else:    
        cur.execute("UPDATE dev.tasks SET status = 1 WHERE task_id=%s;", (task_id,))
  except Exception as e:
    print(e)
    raise(e) 

  conn.commit()
  cur.close()
  conn.close()

def delete_task(task_id):
  conn = connectToDB()
  cur = conn.cursor()

  try:
    cur.execute("UPDATE dev.tasks SET status = -1 WHERE task_id=%s;", (task_id,))  
    # cur.execute("DELETE FROM dev.tasks WHERE task_id=%s;", (task_id,))
    # print("db.delete_task: DELETE FROM dev.tasks WHERE taskid=%s;" % task_id)
  except Exception as e:
    print(e)
    raise(e) 

  conn.commit()
  cur.close()  
  conn.close()  

def purge_tasks(user_id):
    conn = connectToDB()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM dev.tasks WHERE status=-1 AND user_id=%s;", (user_id,))
    except Exception as e:
        conn.rollback()
        conn.close()
        print(e)
        raise(e)

    conn.commit()
    cur.close()
    conn.close()

    

    




