import json
import socket
from communication_json import convert2send, readall

def sendAttendanceData(teacher_id, class_id, subject_code, attendance_request, attendance_server):
    data = {}
    if teacher_id != None:
        data['tid'] = teacher_id
    if class_id != None:
        data['cid'] = class_id
    if subject_code != None:
        data['scode'] = subject_code
    data['attendance'] = attendance_request
    #convert the data to be sent into json format
    datastr = convert2send(data)
    #print(datastr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((attendance_server['host'], attendance_server['port']))
        try:
            #sending attendance start data to server
            sock.sendall(datastr)
            #receive response which is byte representing attendance done or not
            response = communication_json.readall(sock)
            if response.has_key('error'):
                print(response['error'])
                #return response
            else:
                return response #response contains {'student_list': list of students(id, name) for this class, 'acode':attendance code}
        except:
            return {'error': 'error sending data'}
    except:
        return {'error': 'server not avialable'}
    
def startAttendance(teacher_id, class_id, subject_code, attendance_server = {'host':'127.0.0.1' , 'port':60001}):
    response = sendAttendanceData(teacher_id, class_id,'start', attendance_server)

def getAttendance(teacher_id, class_id, attendance_server = {'host':'127.0.0.1' , 'port':60001}):
    response = sendAttendanceData(teacher_id, class_id, None, 'get', attendance_server) #doesn't require subject to be specified to get attendance

def stopAttendance(teacher_id, class_id, attendance_server = {'host':'127.0.0.1' , 'port':60001}):
    response = sendAttendanceData(teacher_id, class_id, None, 'stop', attendance_server) #doesn't require subject to be specified to close attendance

def updateClassAndSubjects(attendance_server = {'host':'127.0.0.1' , 'port':60001}):
    response = sendAttendanceData(None,None,None,'update',attendance_server)
    
if __name__ == '__main__':
    #start attendance
    startAttendance('bct12', 'bctcd','mp')
    #wait some time
    #get realtime attendance ststus
    getAttendance('bct12', 'bctcd')
    #stop attendance
    stopAttendance('bct12', 'bctcd')
    input()