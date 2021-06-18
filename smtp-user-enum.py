#!/usr/bin/python3

import socket
import sys

if len(sys.argv) !=3:
    sys.exit("Usage: smtp-user-enum.py <smtp ip> <username text file>")

with open(sys.argv[2], 'r') as user_file:
    user_list = user_file.readlines()
    user_file.close

new_user_list = []

try:
    for user in user_list:
        new_user_list.append(user.strip('\n'))   
        #print(user)
except:
    pass

valid_users = []

try:
    print("Testing connection to SMTP service...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect((sys.argv[1], 25))
    banner = s.recv(1024).decode()
    print(banner)
    s.close()
except:
    sys.exit("Unable to connect to SMTP service")

if "220" in banner:
    for u in new_user_list:
        print("Testing user: {}".format(u))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect = s.connect((sys.argv[1], 25))
        banner = s.recv(1024).decode()
        s.send(str.encode("VRFY {} \r\n".format(u)))
        result = s.recv(1024).decode()
        print("\n" + result)
        if "252" in result:
            valid_users.append(u)
else:
    sys.exit("Server seems available, but may require authentication...")

num_users = len(valid_users)
if num_users > 0:
    print("\nFound {} valid users!".format(num_users))
    for user in valid_users:
        print("\nFound user: {}".format(user))
 
