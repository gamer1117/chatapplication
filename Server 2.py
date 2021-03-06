#Server for multithreading chat application

#Importing packages
from socket import *
from threading import Thread

#Sets up constant variables for later use
clients = {}
addresses = {}

HOST = '' #IP that clients connect to. Leave blank to auto-obtain.
PORT = 33000 #The port that is listening for connections.

BUFSIZ = 1024 #Buffer size
ADDR = (HOST, PORT) #Host address, IP and Port
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind(ADDR)

#Gathers a few variables for settings up the server.
hostName = gethostname() #Retrieves device name
hostIP = gethostbyname(hostName) #Retrieves device/host IP
serverName = input("Please name your server: ") #User sets server name

#Creates a function that handles clients into the server
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print ("[SERVER]: Someone has connected from " + str(client_address))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

#Takes client socket as argument.
def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8") #Gets client name on connection
    welcome = 'Welcome to ' + serverName + ', %s' % name #Welcome message
    client.send(bytes(welcome, "utf8")) #Sends welcome message
    msg = "%s has joined the server." % name #Informs other clients of new connection
    print ("[SERVER]: %s has joined the server." % name)
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("/quit", "utf8"):
            broadcast(msg, "<" + name + "> ")
            print("[" + name + "]: " + str(msg))
        else:
            client.send(bytes("You have been disconnected from the server.", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the server." % name, "utf8"))
            print("[SERVER]: %s has left the server." % name)
            break

#Broadcasts message to whole server
def broadcast(msg, prefix=""): #Prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

#Prints multiple variables when called
def info():
    print("|======== INFO ========|")
    print("Jahchat alpha server.")
    print("Server name: " + serverName) #Server name
    print("Host device name: " + hostName) #Device name
    print("Host IP: " + hostIP) #Server/Host IP
    print("Port in use: " + str(PORT)) #Port listening for connections
    print("|======================|")

print("Server created.") #Server has been generated by this point.

#checkVariablesinput(print("Check variables?: ")

#Starts connections
if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    info()
    print("Server open.")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() #Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
    

