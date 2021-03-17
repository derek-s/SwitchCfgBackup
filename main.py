#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek.S
# FILE: main.py
# DATE: 2021/03/17
# TIME: 20:22:52

# DESCRIPTION: main file

import socket
import yaml
from yaml.loader import FullLoader

from sn import snBackup
from tn import tnBackup


def checkPort(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, int(port)))
        server.close()
        return True
    except Exception as e:
        return False

def readConfigFile(path):
    with open(path) as f:
        data = yaml.load(f, Loader=FullLoader)
    return data

if __name__ == "__main__":
    config = readConfigFile("hosts.yml")
    tftpSeverIP = config["tftp_ip"]
    hostsList = config["hosts"]
    for x in hostsList:
        switchIP = str(x["ip"])
        username = str(x["username"])
        password = str(x["password"])
        enPassword = str(x["enPassword"])
        portCon22Result = checkPort(switchIP, 22)
        portCon23Result = checkPort(switchIP, 23)
        if(portCon22Result):
            snBackup(switchIP, username, password, enPassword, tftpSeverIP)
        elif(portCon23Result):
            tnBackup(switchIP, username, password, enPassword, tftpSeverIP)
