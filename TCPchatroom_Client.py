import socket
import threading

sender_nickname = input("Please enter your nickname!!: ")
if sender_nickname == 'admin':
    password = input("Enter the admin password: ")
    

PORT = 6669
HOST =  socket.gethostbyname(socket.gethostname())  #local Host
ADDR = (HOST, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


stop_thread = False

def receiver():
    while True:
        global stop_thread
        if stop_thread == True:
            break
        
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == 'NICK':
                client.send(sender_nickname.encode('ascii'))
                next_msg = client.recv(1024).decode('ascii')
                
                if next_msg == 'PSD':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Access Denied !!")
                        stop_thread = True     
                elif next_msg == 'BAN':
                    print("Access Denied BecoZ of Ban")
                    client.close()
                    stop_thread = True 
                                  
            else:
                print(msg)
        except:
            print("Someting Wrong!!")
            client.close()
            break
        
def write():
    while True:
      if stop_thread == True:
            break
      
      message = f'{sender_nickname}: {input("")}'
      if message[len(sender_nickname) + 2:].startswith('/'):
          
          if sender_nickname == 'admin':
              
              if message[len(sender_nickname) + 2:].startswith('/kick'):
                  client.send(f'KICK {message[len(sender_nickname) + 2 + 6:]}'.encode('ascii'))
              elif message[len(sender_nickname) + 2:].startswith('/ban'):
                  client.send(f'BAN {message[len(sender_nickname) + 2 + 5:]}'.encode('ascii'))
                  
          else:
              print("Only Admin is Authorized")
              
      elif message[len(sender_nickname) + 2:].startswith('+'):
          receiver_nickname = message[len(sender_nickname) + 2 + 2:]
          client.send(f'CONN {receiver_nickname}'.encode('ascii'))
      
      elif message[len(sender_nickname) + 2:].startswith('-'):
          receiver_nickname = message[len(sender_nickname) + 2 + 2:]
          client.send(f'DCONN {receiver_nickname}'.encode('ascii'))
      
      else:
           client.send(message.encode('ascii'))
      
      
receive_thread = threading.Thread(target=receiver)
receive_thread.start()


write_thread = threading.Thread(target=write)
write_thread.start()

