import socket
import threading
import random
import sched, time
import face_recognition
import mysql.connector

import communication_json
import insertdb
import utility

MAX_ACODE = 1000

#server info
server_ip = 'localhost'
student_port = 60000
teacher_port = 60001
#updater_port = 60002

#database info
dbinfo = {'host':'localhost',
           'user': 'root',
           'password': 'Ashutosh123$',
           'port': 3306,
           'database': 'sas'}

ATTENDANCE_TIMEOUT = 10 * 60  #attendance closes automatically after 10 minutes if teacher doesn't close it
ATTENDANCE_TIMEOUT_CHECK = 10  #checks every 10 seconds for timeout of attendance
attendance_scheduler = sched.scheduler(time.time, time.sleep)

##class Attendance:
##    def __init__(self, tid, acode, aid):
##        self.tid = tid
##        self.acode = acode
##        self.aid = aid
        
#insert { classid:(teacherid, acode, aID) } to attendance active to start attendance
active_attendance = {}
#insert { classid: studentids[]} for student whose attendance is left to be shown to corresponding teacher
students_present = {}


def connect2db(_dbinfo = dbinfo):
    '''returns cursor to the mysql database mentioned in dbinfo dictionary'''
    mysqlconn = mysql.connector.connect(host = _dbinfo['host'],user = _dbinfo['user'],password = _dbinfo['password'],
                                        port = _dbinfo['port'],database = _dbinfo['database'])
    mycursor = mysqlconn.cursor()
    return mycursor

def sendSQLserverError(conn):
    response = {}
    response['error'] = 'couldn\'t connect to attendance server. please try again after a moment'
    communication_json.convertSendClose(response, conn)

def studentHandler(conn):
    data = communication_json.readall(conn)
    #print(data)
    response = {}
    #find the class of the student
    class_query = 'SELECT cID FROM student WHERE sID = {}'.format(data['sid'])
    try:
        mycursor = connect2db()
        try:
            mycursor.execute(class_query)
            res = mycursor.fetchone()
            if res == None:
                response['error'] = 'you are not registered for any class'
                communication_json.convertSendClose(response, conn)
                return
            data['cid'] = res[0]
        except:
            raise
        finally:
            mycursor.close()
    except mysql.connector.Error as e:
        print(e)
        sendSQLserverError(conn)
        return
    
    if !active_attendance.has_key(data['cid']):
        response['error'] = 'class is not taking attendance at the moment'
        communication_json.convertSendClose(response, conn)
        return
    else:
        if active_attendance.[data['cid']][1] != data['acode']:
            response['error'] = 'attendance code wrong'
            communication_json.convertSendClose(response, conn)
            return
        elif data['sid'] in students_present[data['cid']]:
            response['error'] = 'Attendance already marked'
            communication_json.convertSendClose(response, conn)
            return
        else:
            try:
                mycursor = connect2db()
                try:
                    #*first check the student is registered for classid*
                    student_facedata_query = 'SELECT embedding FROM facedata WHERE sID = {} ORDER BY index'.format(data['sid'])
                    mycursor.execute(student_facedata_query)
                    result = mycursor.fetchall()
                    facedata = []
                    if len(result) == 0:
                        response['error'] = 'Your face is not registered. Contact the administrator'
                    elif len(result) != 128:
                        print('Face data insufficient in database')
                        sendSQLserverError(conn)
                        return
                    else:
                        for res in result:
                            facedata.append(res[0])
                        #compare facedata
                        match = face_recognition.compare_faces(facedata, data['face'])
                        if match[0]:
                        #if face match then update
                            mark_attendance_query = 'UPDATE record SET presence = true WHERE aID = {}'.format(active_attendance.[data['cid']][2])
                            mycursor.execute(student_facedata_query)
                            #add student_id to students_present[];
                            students_present[data['cid']].append(data['sid'])
                            #send attendance status to 'socket' and save in database;
                            response['success'] = 'Attendance marked'
                            communication_json.convertSendClose(response, conn)
                            return
                        else
                            response['error'] = 'Face didn\'t match. Please try again'
                            communication_json.convertSendClose(response, conn)
                            return
                except mysql.connector.Error as e:
                    sendSQLserverError(conn)
                    return
                finally:
                    mycursor.close()
            except mysql.connector.Error as e:
                sendSQLserverError(conn)
                return

def studentConnectionListen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sl:
        sl.bind((server_ip, student_port))
        while(True):
            sl.listen()
            conn, addr = sl.accept()
            #start new thread;
            t = threading.Thread(target= studentHandler, args = (conn,))
            t.start()
            print("Connected to student at: ", addr)

def removeClassFromAttendance(class_id):
    if active_attendance.hasKey(class_id):
        del active_attendance[class_id]  #remove the class from active attendance list
        del students_present[class_id]   #remive students list

def attendanceTimeout():
    #see time of each started attendance in active_attendance and close if maximum time has elapsed
    while True:
        if attendance_scheduler.empty():
            time.sleep(ATTENDANE_TIMEOUT_CHECK)
        else:
            attendance_scheduler.run()
    
    
##def teacherAttendanceLogFeedback(conn, class_id):
##    #if student_present[] is not empty send the student_ids and remove from the list
##    #close this thread if corresponding class_id has been removed from active attendance list
##    return
##
##def getStudentList_json(class_id):
##    #get student list and their id from database for class_id
##    #save it in proper python structure
##    #return the json format data
##    return
##
####def teacherExists(db_cursor):
####    return

def getNewAttendanceCode(_ACODE = ACODE):
    #select a random unique number as code
    acode_unique = False
    while !acode_unique:
        acode = random.randint(0,_ACODE)
        acode_unique = True
        for key in active_attendance:
            if active_attendance[key][1] == acode:
                acode_unique = False
                break
    return acode

def teacherHandler(conn):
    data = communication_json.readall(conn)
    response = {}
    #check if attendance is in progress or not to start/stop attendance
    if data['attendance'] == 'end':
        #stopping attendance
        if active_attendance.hasKey(data['cid']):
            if active_attendance[data['cid']][0] == data['tid']:
                #same teacher must close attendance 
                del active_attendance[data['cid']]  #remove the class from active attendance list
                del students_present[data['cid']]   #remive students list
                response['success'] = 'attendance stopped'
                communication_json.convertSendClose(response, conn)
                return
                #perform other cleanup...
            else:
                response['error'] = 'another teacher started attendance for this class'
                communication_json.convertSendClose(response, conn)
                return
        else:
            response['error'] = 'no attendance in progress for the class'
            communication_json.convertSendClose(response, conn)
            return
            
     elif data['attendance'] == 'start':
         #starting attendance
         if active_attendance.hasKey(data['cid']):
            response['error'] = 'attendance already started'
            communication_json.convertSendClose(response, conn)
            return
        #check the classid and teacherid in data are correct consulting database
        try:
            mycursor = connect2db()
            try:
                teacher_exists_query = 'SELECT tID FROM sas.teacher WHERE tID = {}'.format(data['tid'])
                mycursor.execute(teacher_exists_query)
                res = mycursor.fetchone()
                if res == None:
                    mycursor.close()
                    response['error'] = 'you are not registered as teacher'
                    communication_json.convertSendClose(response, conn)
                    return
                else:
                    class_exists_query = 'SELECT cID FROM sas.class WHERE cID = {}'.format(data['cid'])
                    mycursor.execute(class_exists_query)
                    res = mycursor.fetchone()
                    if res == None:
                        response['error'] = 'couldn\'t find class'
                        communication_json.convertSendClose(response, conn)
                        return
                    else:
                        subject_exists_query = 'SELECT scode FROM sas.subject WHERE scode = {}'.format(data['scode'])
                        mycursor.execute(class_exists_query)
                        res = mycursor.fetchone()
                        if res == None:
                            response['error'] = 'couldn\'t find subject'
                            communication_json.convertSendClose(response, conn)
                            return
                        else:
                            #a unique attendance identifier for current session
                            acode = getNewAttendanceCode()
                            #send student list with studentid, name and attendance code
                            classlist_query = 'SELECT sID, name FROM student WHERE cID = {}'.format(data['cid'])
                            mycursor.execute(classlist_query)
                            result = mycursor.fetchall()
                            response['student_list'] = result
                            response['acode'] = acode
                            response['timeout'] = 'the attendance will close automatically in {} minoutes if not explicitly closed'.format(TIMEOUT_ATTENDANCE)
                            communication_json.convertSendClose(response, conn)
                            sidlist = [r[0] for r in result]
                            
                            #make new attendance record in database
                            attendanceid = insertdb.insertAttendance(data['tid'], data['scode'], data['cid'])
                            insertdb.insertRecords(attendanceid, sidlist)   #adding records of students to the attendance for the respective class with default false for presence
                            #add the classid:teacherid pair to active attendance list
                            active_attendance[data['cid']] = (data['tid'], acode, attendanceid)
                            students_present[data['cid']] = [] #initially no student present
                            #stop attendance after timeout period if teacher doesn't close explicitly
                            attendance_scheduler.enter(ATTENDANCE_TIMEOUT, 0 ,removeClassFromAttendance, argument=(data['cid'],))
                            #--- start new thread for attendance log feedback  --- not applicable now
                            #--- wait for attendance stop message from teacher client  --- not applicable now
            except mysql.mysql.connector.Error as e:
                sendSQLserverError(conn)
                return
            finally:
                mycursor.close()
        except mysql.mysql.connector.Error as e:
            sendSQLserverError(conn)
            return
    elif data['attendance'] == 'get':
        #send list of students whose attendance has been marked
        if active_attendance.hasKey(data['cid']):
            if active_attendance[data['cid']][0] == data['tid']:
                #same teacher is only allowed to see realtime attendance data
                response['student_list'] = students_present[data['tid']]
                communication_json.convertSendClose(response, conn)
                return
            else:
                response['error'] = 'another teacher started attendance for this class'
                communication_json.convertSendClose(response, conn)
                return
        else:
            response['error'] = 'no attendance in progress for the class'
            communication_json.convertSendClose(response, conn)
            return
    elif data['attendance'] == 'update':
        #though the key is 'attendance' it has nothing to do with attendance
        #this just sends updated list of class and subjects to teacher
        classSubjectUpdater(conn)
        return

def teacherConnectionListen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_ip, teacher_port))
        while(True):
            s.listen()
            conn, addr = s.accept()
            #start new thread;
            t = threading.Thread(target= teacherHandler, args = (conn,))
            t.start()
            print("Connected to teacher at: ", addr)


#class and subject data updater for teacher
def classSubjectUpdater(conn):
    data = communication_json.readall(conn)
    response = {}
    try:
        mycursor = connect2db()
        try:
            classlist_query = 'SELECT cID, name FROM class WHERE 1'
            mycursor.execute(classlist_query)
            result = mycursor.fetchall()
            response['class'] = result
            subjectlist_query = 'SELECT scode, name FROM subject WHERE 1'
            mycursor.execute(subjectlist_query)
            result = mycursor.fetchall()
            response['subject'] = result
            communication_json.convertSendClose(response, conn)
        except:
            raise
        finally:
            mycursor.close()
    except:
        sendSQLserverError(conn)
        return

##def UpdateConnectionListen():
##    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
##        s.bind((server_ip, teacher_port))
##        while(True):
##            s.listen()
##            conn, addr = s.accept()
##            #start new thread;
##            t = threading.Thread(target= classSubjectUpdater, args = (conn,))
##            t.start()
##            print("Connected to teacher at: ", addr)
    

if __name__ == '__main__':
    
    
    
