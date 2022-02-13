import json
import socket
from communication_json import convert2send

attendance_server = {'host':'127.0.0.1' , 'port':60000}

def markAttendance(student_id, acode, face_embd, _attendance_server = attendance_server):    
    data = {}
    data['sid'] = student_id
    data['acode'] = acode
    data['face'] = face_embd
    #convert the data to be sent into json format
    datastr = communication_json.convert2send(data)
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
            elif response.has_key('success'):
                print(response['success'])
                #return response #response contains 
        except:
            return {'error': 'error sending/receiving data'}
    except:
        return {'error': 'server not avialable'}

if __name__ == '__main__':
##    markAttendance('075bct052', '88', 
##                 [0.258, 0.444447, 0.1258, 0.36697, 0.125887, 0.11245588])
    input()
