#JahChat client

#Importing packages
#from socket import AF_INET, socket, SOCK_STREAM
from socket import *
from threading import *
import tkinter
from tkinter import *
from tkinter import messagebox

#These are here to stop the program breaking later on
HOST = 1
PORT = 1
BUFSIZ = 1024
client_socket = socket(AF_INET, SOCK_STREAM)

#<!---- Functions and Protocols ---->

#Connects to a server. Called by btnConnect.
def connect():

    #Defines variables as global.
    global HOST
    global PORT
    global ADDR
    global receive_thread
    global client_socket

    #Gathers Host and Port from user input.
    HOST = etyHost.get()
    PORT = etyPort.get()


    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    #Connects client to server.
    client_socket = socket(AF_INET, SOCK_STREAM)
    print("!")
    BUFSIZ = 1024
    print("!!")
    ADDR = (HOST, PORT)
    print("!!!")
    client_socket.connect(ADDR)
    print("!!!!")

    receive_thread = Thread(target=receive)
    print("recieved")
    receive_thread.start()
    print("Thread started")
    connected = True
    try:
        clientName
    except NameError:
        msgChatlog.insert(END, "Please use a valid name. You will be disconnected from the server.")
        return
    else:
        junk = "code"

    client_socket.send(bytes(clientName, "utf8"))

#Disconnects the user from the server
def disconnect():
    msg = "/quit"
    client_socket.send(bytes(msg, "utf8"))
      
#Receives messages from server.
def receive():

    #While loop is active, all messages are received.
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msgChatlog.insert(END, msg)
        except OSError as e:
            print('OSError, break:{}'.format(e))
            msgChatlog.insert(END, "Your connection to the server has been lost.")
            break

#Sends message as bytes to connected server.
def send(event=None):  #Event is passed by binders.
    
    msg = varMessage.get()
    varMessage.set("")
    client_socket.send(bytes(msg, "utf8"))


#When window is closed, send "/quit" to server.
def on_closing(event=None):
    try:
        varMessage.set("/quit")
        send()
        jahchat.destroy()
    except OSError as e:
        jahchat.destroy()

#Creates an entirely new window for settings
def settingsWindow():

    #Applies settings changes
    def changeName():
        global clientName
        clientName = etyName.get()
        
    #Changes the color of the windows
    def changeColor():
        jahchat.config(background = varColor.get())
        jahchatSettings.config(background = varColor.get())

    #Creates the settings window
    jahchatSettings = Tk()
    jahchatSettings.geometry("500x500")
    jahchatSettings.config(background = "Orange")
    jahchatSettings.resizable(False, False)
    jahchatSettings.title("JahChat Settings")

    #Creates a label for 'Name'
    lblName = Label(jahchatSettings, text = "Name:")
    lblName.config(height = 1, width = 20)
    lblName.pack()
    lblName.place(x = 0, y = 0)

    #Creates an entry box for 'Name'
    etyName = Entry(jahchatSettings)
    etyName.config(width = 40)
    etyName.pack()
    etyName.place(x = 150, y = 1)

    #Creates a button for 'Name'
    btnApply = Button(jahchatSettings, text = "Change Name", command = changeName)
    btnApply.config(width = 20)
    btnApply.place(x = 0, y = 100)

    #Creates an option menu for 'Color'
    varColor = StringVar(jahchatSettings)
    varColor.set("Orange")
    
    colors = [
        "Orange",
        "Blue",
        "Red",
        "Green",
        "Black"
    ]
    
    opnColor = OptionMenu(jahchatSettings, varColor, *colors)
    opnColor.config(width = 20)
    opnColor.pack()
    opnColor.place(x = 0, y = 30)


    #Creates a button for 'Color'
    btnColor = Button(jahchatSettings, text = "Change Color", command = changeColor)
    btnColor.config(width = 20)
    btnColor.place(x = 250, y = 250)
    
    jahchatSettings.mainloop()

#<!---- GUI ---->

#Creates window.
jahchat = Tk()
jahchat.geometry("500x500")
jahchat.config( background = "orange")
jahchat.resizable(False, False)
jahchat.title("JahChat")

jahchat.protocol("WM_DELETE_WINDOW", on_closing)

#Var message is what goes into the chat
varMessage = StringVar()  # For the messages to be sent.
varMessage.set("Type your messages here.")

#Scrollbar for the chatlog
srlChatlog = Scrollbar()  # To navigate through past messages.

#Listbox widget
msgChatlog = Listbox(jahchat)
msgChatlog.config(height=15, width = 80, yscrollcommand=srlChatlog.set)
srlChatlog.pack(side = RIGHT, fill = Y)
msgChatlog.pack()
msgChatlog.place(x = 0, y = 0)

#Send messages
etyMessage= Entry(textvariable=varMessage)
etyMessage.bind("<Return>", send)
etyMessage.pack()
etyMessage.place(x = 250, y = 250)

btnMessage = Button(text="Send", command=send)
btnMessage.pack()
btnMessage.place(x = 250, y = 265)

#Entry box
etyHost = Entry(jahchat)
etyHost.pack()
etyHost.place(x = 0, y = 250)

#Entry box
etyPort = Entry(jahchat)
etyPort.pack()
etyPort.place(x = 0, y = 275)

#Button
btnConnect = Button(jahchat, text = "Connect", command = connect)
btnConnect.config(width = 20)
btnConnect.place(x = 0, y = 320)

#Button
btnDisconnect = Button(jahchat, text = "Disconnect", command = disconnect)
btnDisconnect.config(width = 20)
btnDisconnect.place(x = 0, y = 350)

#Settings button
btnSettings = Button(jahchat, text = "Settings", command = settingsWindow)
btnSettings.config(width = 20)
btnSettings.place(x = 50, y = 400)

jahchat.mainloop()  # Starts GUI execution.
