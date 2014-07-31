#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import thread
import time
concts = {}
s = socket.socket()# Create a socket object
host = raw_input("Local IP: ") # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

def connect():
   global s
   global concts
   s.listen(5)
   while True:
      c, addr = s.accept()
      name = c.recv(16)
      if not name in concts:
         print 'Got connection from',name,'at',addr
         c.send('Welcome the chat '+name+'!')
         concts[name] = c
         thread.start_new_thread(relay,(c,name))
      else:
         c.send('Sorry the name '+name+' is taken!')
         c.close()
          

def relay(c,name):
   global s
   global concts
   running = True
   for k,d in concts.items():
               if d != c:
                  d.send(name+" has entered the room!")
   while running:
         data = c.recv(512)
         if data:
            print data
            if data == name+": /quit":
               c.close()
               data = name+" Disconnected!"
               print data
               running = False
            for k,d in concts.items():
               if d != c:
                  d.send(data)
   del concts[name]
   return False

thread.start_new_thread(connect,())
      
