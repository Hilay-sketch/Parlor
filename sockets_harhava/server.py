import json
import socket

import mainParlor as MainSim
import protocol as pr
from IceParlorExceptionF import SocketParlorError

configurations = {}


def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", pr.PORT))
        server_socket.listen()
        print("Server is up and running")
    except Exception as e:
        print(f"Server is not working try somthing else {e}")
        raise SocketParlorError(e)

    (client_socket, client_address) = server_socket.accept()
    client_address = client_address[0]
    print(f"Client connected: {client_address}")

    cmd, data = pr.get_command(client_socket)
    print(cmd, data)
    while cmd != pr.Commands.EXIT:
        if cmd == pr.Commands.SET_CONFIG:
            configurations[client_address] = data
            print(configurations)
            client_socket.sendall(pr.create_msg('Configuration set successfully'))
        elif cmd == pr.Commands.GET_CONFIG:
            if client_address in configurations:
                client_socket.sendall(pr.create_msg(configurations[client_address]))
            else:
                client_socket.sendall(pr.create_msg('No configuration found for this IP'))
        elif cmd == pr.Commands.ACTIV_FUN:
            config_data = json.loads(configurations[client_address])
            action = data
            config_data["simulation"]["action"] = action
            parlors = MainSim.load_ice_cream_list(config_data.get("parlors", {}))
            customers = MainSim.load_customer_list(config_data)
            simulation = MainSim.ParlorSimulation(customers, parlors)
            result = MainSim.choosing_action(action, simulation)
            # Convert the result to JSON and send it back to the client
            client_socket.sendall(pr.create_msg(json.dumps(result)))
        else:
            response = f"Wrong protocol command{cmd}:{data}"
            response = pr.create_msg(response)
            client_socket.sendall(response)
        cmd, data = pr.get_command(client_socket)

    print("Closing\n")


def main():
    start_server()


if __name__ == "__main__":
    main()
