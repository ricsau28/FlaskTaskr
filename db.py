#flask-taskr/db.pyimport psycopg2 as psy
import psycopg2 as psy
import psycopg2.extras as psyextra


CONNECTION_STRING = ''
COMMIT = 1
ROLLBACK = -1

def init(connection_string):
    global CONNECTION_STRING
    CONNECTION_STRING = connection_string    

def connectToDB():
    try:
        return psy.connect(CONNECTION_STRING)
    except psy.OperationalError as oe:
        print("db.connectToDB: {}".format(oe))    
        raise(e)
    except Exception as e:
        print("db.connectToDB: {}".format(e))    
        raise(e)

def connectToDBAndGetCursor():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory = psy.extras.DictCursor)
  return conn, cur

def closeConnection(conn, cur = None, action = None):  
  # commit or rollback transaction
  if action in (COMMIT, ROLLBACK):
    try:
      if action == COMMIT:
        conn.commit()
      elif action == ROLLBACK:
        conn.rollback()  
    except Exception as e:
      print(e.pgcode)
      print(e)
      print("db.closeConnection: Error committing/rolling back.")    
      raise(e)

  # close the cursor
  try:    
    if cur != None:
      cur.close()
  except Exception as e:
    print(e.pgcode)
    print(e)
    print("db.closeConnection: Error closing cursor.")    
    raise(e)

  #finally, close the connection
  try:       
    conn.close()
  except Exception as e:
    print(e.pgcode)
    print(e)
    print("db.closeConnection: Error closing connection.")    
    raise(e)

def addNewUser(user):
    conn, cur = connectToDBAndGetCursor()
    
    try:
        cur.execute("INSERT INTO dev.users (user_name, email, password, role) VALUES(%s, %s, %s, %s);",
                   (user.name, user.email, user.password, user.role))
    except Exception as e:        
        closeConnection(conn, cur, ROLLBACK)
        if int(e.pgcode) != 23505:
            print("Error code: {0}".format(e.pgcode))
            print(e)
            raise(e)           
        return False
    
    closeConnection(conn, cur, COMMIT)
    return True
    

def getUserCredentials(user, pwd):
    #conn = connectToDB()
    #cur = conn.cursor(cursor_factory = psy.extras.DictCursor)
    conn, cur = connectToDBAndGetCursor()
    try:
        cur.execute("SELECT user_id, role, password FROM dev.users WHERE user_name = %s AND password = %s;", (user,pwd))
    except Exception as e:
        #raise e
        print(e)
        return None

    result = cur.fetchone()
    closeConnection(conn, cur)
    return result

# ===============  Task-related operations  ==============

def getTaskInfo(taskID):
  conn, cur = connectToDBAndGetCursor()

  try:
    cur.execute("SELECT task_id, task_name, due_date, priority FROM dev.tasks WHERE task_id = %s;", (taskID,))
    #cur.execute('select name, due_date, priority, task_id from tasks where status=0')
  except Exception as e:
    #Log e
    raise(e) 

  result = cur.fetchone()
  closeConnection(conn, cur)  
  return result


def getOpenTasks(user_id):
  conn, cur = connectToDBAndGetCursor()

  try:
    # TODO: Change dev.tasks to tasks in production 10/2/2018  
    cur.execute('select task_name, due_date, priority, task_id from dev.tasks where status=1 AND user_id=%s;',(user_id,))
  except Exception as e:
    print(e)
    raise(e)

  results = cur.fetchall()
  closeConnection(conn, cur)
  return results         

def getClosedTasks(user_id):
  conn, cur = connectToDBAndGetCursor()

  try:
    cur.execute('select task_name, due_date, priority, task_id from dev.tasks where status=0 AND user_id=%s;',(user_id,))
  except Exception as e:
    print(e)
    raise(e)

  results = cur.fetchall()
  closeConnection(conn, cur)
  return results     

def add_task(user_id, taskname, duedate, priority, status):
  conn, cur = connectToDBAndGetCursor()
  
  try:
    #cur.execute('select task_name, due_date, priority, task_id from tasks where status=0')
    cur.execute("INSERT INTO dev.tasks (user_id, task_name, due_date, priority, status) VALUES (%s, %s, %s, %s, %s);",
                (user_id, taskname, duedate, priority, 1))

  except Exception as e:
    print("INSERT INTO dev.tasks (user_id, task_name, due_date, priority, status) VALUES ({}, {}, {}, {}, {});".format(
          user_id, taskname, duedate, priority, status))
    print(e)
    closeConnection(conn, cur, ROLLBACK)
    raise(e)
    
  closeConnection(conn, cur, COMMIT)
  

def update_task(task_id, taskname, duedate, priority):
  conn, cur = connectToDBAndGetCursor()

  try:
    cur.execute("UPDATE dev.tasks SET task_name=%s, due_date=%s, priority=%s WHERE task_id=%s;", 
                (taskname, duedate, priority, task_id))
  except Exception as e:    
    print(e)
    closeConnection(conn, cur, ROLLBACK)
    raise(e) 

  closeConnection(conn, cur, COMMIT)

def update_task_complete(task_id, task_completed=False):
  conn, cur = connectToDBAndGetCursor()

  try:
    if task_completed == True:  
        cur.execute("UPDATE dev.tasks SET status = 0 WHERE task_id=%s;", (task_id,))
    else:    
        cur.execute("UPDATE dev.tasks SET status = 1 WHERE task_id=%s;", (task_id,))
  except Exception as e:
    print(e)
    closeConnection(conn, cur, ROLLBACK)
    raise(e) 

  closeConnection(conn, cur, COMMIT)

def delete_task(task_id):
  conn, cur = connectToDBAndGetCursor()

  try:
    cur.execute("UPDATE dev.tasks SET status = -1 WHERE task_id=%s;", (task_id,))  
    # cur.execute("DELETE FROM dev.tasks WHERE task_id=%s;", (task_id,))
    # print("db.delete_task: DELETE FROM dev.tasks WHERE taskid=%s;" % task_id)
  except Exception as e:
    print(e)
    closeConnection(conn, cur, ROLLBACK)
    raise(e) 

  closeConnection(conn, cur, COMMIT)

def purge_tasks(user_id):
    conn, cur = connectToDBAndGetCursor()

    try:
        cur.execute("DELETE FROM dev.tasks WHERE status=-1 AND user_id=%s;", (user_id,))
    except Exception as e:
        print(e)
        closeConnection(conn, cur, ROLLBACK)
        raise(e)

    closeConnection(conn, cur, COMMIT)

    

    




