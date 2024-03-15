import socket
import protocol as pr
from IceParlorExceptionF import SocketParlorError

s = socket.socket()


def start_client():
    try:
        s.connect(('192.168.1.209', pr.PORT))
        print("possible commands: SET_CONFIG, GET_CONFIG, ACTIV_FUN {function_name}, EXIT")
        client_command = input("Enter a command: ")
        while client_command != "EXIT":
            if client_command == "SET_CONFIG":
                with open("current_client_config.json", "r") as f:
                    config = f.read()
                s.sendall(pr.create_msg(client_command + ' ' + config))
                print(pr.get_command_client(s))
            elif client_command == "GET_CONFIG":
                s.sendall(pr.create_msg(client_command))
                with open("current_client_config.json", "w") as f:
                    f.write(pr.get_command_client(s))
            elif client_command.startswith("ACTIV_FUN"):
                s.sendall(pr.create_msg(client_command))
                with open("current_client_config.json", "w") as f:
                    f.write(pr.get_command_client(s))
            print("possible commands: SET_CONFIG, GET_CONFIG, ACTIV_FUN {function_name}, EXIT")
            client_command = input("Enter a command: ")
        s.close()
    except Exception as e:
        print(f"Client is not working try somthing else {e}")
        raise SocketParlorError(e)


def main():
    start_client()


if __name__ == "__main__":
    main()
