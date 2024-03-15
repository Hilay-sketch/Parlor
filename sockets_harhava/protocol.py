import enum
import socket
import struct

PORT = 5050


class Commands(enum.Enum):
    SET_CONFIG = 0
    GET_CONFIG = 1
    ACTIV_FUN = 2
    ERR = 3
    EXIT = 4


def check_cmd(data):
    if data not in Commands:
        return False
    return True


def create_msg(data):
    d = data.encode()
    length = len(d)
    length_bytes = struct.pack('!H', length)
    buffer = length_bytes + d
    return buffer


def get_command(my_socket: socket.socket):
    length_bytes = recv_amount(my_socket, 2)
    length = struct.unpack('!H', length_bytes)[0]
    com = recv_amount(my_socket, length)
    com = com.decode()
    try:
        for cmd in Commands:
            if com.startswith(cmd.name):
                return cmd, com[len(cmd.name):].strip()
        return Commands.ERR, ""
    except KeyError:
        return Commands.ERR, ""


def get_command_client(my_socket: socket.socket):
    length_bytes = recv_amount(my_socket, 2)
    length_num = struct.unpack("!H", length_bytes)
    com = recv_amount(my_socket, length_num[0])
    com = com.decode()
    return com


def recv_amount(my_socket, amount):
    buffer = b''
    while len(buffer) < amount:
        buffer += my_socket.recv(amount - len(buffer))
    return buffer
