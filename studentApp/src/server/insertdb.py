import mysql.connector

dbinfo = {'host':'localhost',
           'user': 'root',
           'password': 'Ashutosh123$',
           'port': 3306,
           'database': 'sas'}

def connect2db(_dbinfo = dbinfo):
    '''returns cursor to the mysql database mentioned in dbinfo dictionary'''
    mysqlconn = mysql.connector.connect(host = _dbinfo['host'],user = _dbinfo['user'],password = _dbinfo['password'],
                                        port = _dbinfo['port'],database = _dbinfo['database'])
    mycursor = mysqlconn.cursor()
    return mysqlconn, mycursor



def insertClass(classid, name):
    query = 'INSERT INTO class(cID, name) VALUES("{0}","{1}")'.format(classid, name)
    try:
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(query)
            mysqlconn.commit()
            print(f'Added ({classid}, {name}) to class table')
            return True
        except mysql.connector.Error as e:
            print(e)
            return False
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return False


def insertSubject(scode, name):
    query = 'INSERT INTO subject(scode, name) VALUES("{0}","{1}")'.format(scode, name)
    try:
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(query)
            mysqlconn.commit()
            print(f'Added ({scode}, {name}) to subject table')
            return True
        except mysql.connector.Error as e:
            print(e)
            return False
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return False

def insertDepartment(depid, name):
    query = 'INSERT INTO department(dID, name) VALUES("{0}","{1}")'.format(depid, name)
    try:
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(query)
            mysqlconn.commit()
            print(f'Added ({depid}, {name}) to department table')
            return True
        except mysql.connector.Error as e:
            print(e)
            return False
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return False

def insertTeacher(tid, name, depid):
    query = 'INSERT INTO teacher(tID, name, dID) VALUES("{0}","{1}","{2}")'.format(tid, name, depid)
    try:
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(query)
            mysqlconn.commit()
            print(f'Added ({tid},{name},{depid}) to teacher table')
            return True
        except mysql.connector.Error as e:
            print(e)
            return False
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return False

def insertStudent(stuid, name, classid, depid, face_embd):
    if len(face_embd) != 128:
        print('face embeddings size not equal to 128')
        return False
    student_query = 'INSERT INTO student(sID, name, cID, dID) VALUES("{0}","{1}","{2}","{3}")'.format(stuid, name, classid, depid)
    face_query = 'INSERT INTO facedata(sID, `index`, `embedding`) VALUES ("{0}", {1}, {2})'.format(stuid, 0, face_embd[0])
    for i in range(127): #first embedding value already in string
        newrow = ',("{0}", {1}, {2})'.format(stuid, i+1, face_embd[i+1])
        face_query += newrow
    try:
        #print(face_query)
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(student_query)
            print(f'Added ({stuid}, {name}, {classid}) to student table')
            #mysqlconn.commit()
            mycursor.execute(face_query)
            mysqlconn.commit()
            print(f'Added facedata of {name}')
            return True
        except mysql.connector.Error as e:
            print(e)
            return False
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return False

def insertAttendance(tid, scode,  cid):
    '''inserts new attendance details and returns its aID if successfull'''
    query = 'INSERT INTO attendance(tID, scode, cID) VALUES("{0}","{1}","{2}")'.format( tid, scode, cid)
    try:
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(query)
            aid = mycursor.lastrowid   #get the auto incremented value of aid for the newly inserted record
            mysqlconn.commit()
            print(f'Added ({aid},current time,{tid},{scode},{cid}) to attendance table')
            return aid
        except mysql.connector.Error as e:
            print(e)
            return None
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return None

def insertRecord(aid, stuid, presence):
    query = 'INSERT INTO record(aID, sID, presence) VALUES({0},"{1}",{2})'.format(aid, stuid, presence)
    try:
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(query)
            print(f'Added ({aid},{stuid},{presence}) to record table')
            mysqlconn.commit()
            return True
        except mysql.connector.Error as e:
            print(e)
            return False
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return False

def insertRecords(aid, stuids, presences = None):
    if presences == None:
        presences = [False for x in range(len(studids))]
    elif len(stuids) != len(presences):
        print('Size of student and presence list not equal')
        return False
    #save attendance records for multiple students in single query
    query = 'INSERT INTO record(aID, sID, presence) VALUES({0},"{1}",{2})'.format(aid, stuids[0], presences[0])
    for i in range(len(stuids)-1): #first value already in query string as it shouldn't have comma at begining
        newrow = ',({0}, {1}, {2})'.format(aid, stuids[i+1], presences[i+1])
        face_query += newrow
    try:
        mysqlconn, mycursor = connect2db()
        try:
            mycursor.execute(query)
            mysqlconn.commit()
            print(f'Added attendance records to record table')
            return True
        except mysql.connector.Error as e:
            print(e)
            return False
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        return False
    
