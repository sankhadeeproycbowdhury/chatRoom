import socket
import threading

PORT = 6669
HOST =  socket.gethostbyname(socket.gethostname())  #local Host
ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = []
sender_nicknames = []


def handle_lateral(client , client_to_send):
    while True:
         try:
             msg = client.recv(1024)
             if msg.decode('ascii').startswith('DCONN'):
                 client_to_send.send("Sender Closed The personal chat!".encode('ascii'))
                 thread = threading.Thread(target= handle , args=(client,) )
                 thread.start()
                 break
             
             elif msg.decode('ascii').startswith('CONN'):
                receiver_nickname = msg.decode('ascii')[5:]
                sender_nickname = sender_nicknames[clients.index(client)]
                    
                if receiver_nickname in sender_nicknames:
                    index = sender_nicknames.index(receiver_nickname)
                    client_to_send2 = clients[index]
                    client_to_send2.send(f"You are Connected with {sender_nickname} !".encode('ascii'))
                    thread = threading.Thread(target= handle_lateral , args=(client,client_to_send2,) )
                    thread.start()
                    continue
                
             client_to_send.send(msg)
             
         except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                sender_nickname = sender_nicknames[index]
                broadcast(f"{sender_nickname} left the Group !!".encode('ascii'))
                sender_nicknames.remove(sender_nickname)
                break
            

def broadcast(msg):
    for client in clients:
        client.send(msg)
        

def kick_user(name):
    if name in sender_nicknames:
        index = sender_nicknames.index(name)
        client_to_kick = clients[index]
        clients.remove(client_to_kick)
        client_to_kick.send("You are kicked by the admin !".encode('ascii'))
        client_to_kick.close()
        sender_nicknames.remove(name)
        broadcast(f"{name} is kicked out by the Admin !".encode('ascii'))        


def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            
            if msg.decode('ascii').startswith('KICK'):
                if sender_nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                    print(f'{name_to_kick} is kickedOut !')
                else:
                    client.send("Command is Refused".encode('ascii'))
                    
            elif msg.decode('ascii').startswith('BAN'):
                if sender_nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('ban.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} is banned !') 
                else:
                    client.send("Command is Refused".encode('ascii'))
                    
            elif msg.decode('ascii').startswith('CONN'):
                receiver_nickname = msg.decode('ascii')[5:]
                sender_nickname = sender_nicknames[clients.index(client)]
                    
                if receiver_nickname in sender_nicknames:
                    index = sender_nicknames.index(receiver_nickname)
                    client_to_send = clients[index]
                    client_to_send.send(f"You are Connected with {sender_nickname} !".encode('ascii'))
                    thread = threading.Thread(target= handle_lateral , args=(client,client_to_send,) )
                    thread.start()
                    break
                
                else:
                    client.send(f"{receiver_nickname} User does't exists!!".encode('ascii'))
                      
            else:
                   broadcast(message)
                
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                sender_nickname = sender_nicknames[index]
                broadcast(f"{sender_nickname} left the Group !!".encode('ascii'))
                sender_nicknames.remove(sender_nickname)
                break
        
        
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")
        
        client.send("NICK".encode('ascii'))
        sender_nickname = client.recv(1024).decode('ascii')
                
        with open('ban.txt' , 'r') as f:
            bans = f.readlines()
            
            if sender_nickname + '\n' in bans:
                client.send("BAN".encode('ascii'))
                client.close()
                continue
        
        if sender_nickname == 'admin':
            client.send("PSD".encode('ascii'))
            password = client.recv(1024).decode('ascii')
            
            if password != 'admin':
                client.send("REFUSE".encode('ascii'))
                client.close()
                continue
             
        
        sender_nicknames.append(sender_nickname)
        clients.append(client)
        
        print(f"nicknamen of clinet is {sender_nickname}")
        broadcast(f"{sender_nickname} joined the group!!".encode('ascii'))
        client.send("connect to server!!".encode('ascii'))
        
        thread = threading.Thread(target= handle , args=(client,) )
        thread.start()


print("Server is listioning...")
receive()

