#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek.S
# FILE: sn.py
# DATE: 2021/03/17
# TIME: 18:12:55

# DESCRIPTION: SSH protocol connect and backup

import paramiko
import re
import time

def snBackup(switchIP, username, password, enPassword, tftpSeverIP):
    trans = paramiko.Transport((switchIP, 22))
    try:
        trans.connect(username=username, password=password)
        ssh = paramiko.SSHClient()
        ssh._transport = trans

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cmd = ssh.invoke_shell()
        cmd.send("en\n")
        cmd.send(enPassword + "\n")
        time.sleep(1)
        flagX = True
        while(flagX):
            time.sleep(0.02)
            result = cmd.recv(1024)
            result_pwd = re.search(r"Password:", result.decode("utf-8"))
            result_prompt = re.search(r".*#", result.decode("utf-8"))
            result_enPwdErr = re.search(r"% Bad secrets", result.decode("utf-8"))
            
            if(result_prompt):
                cmd.send("copy running-config tftp:\n")
                cmd.send(tftpSeverIP + "\n")
                cmd.send(switchIP + "\n")
                flag = True
                while(flag):
                    time.sleep(0.02)
                    result = cmd.recv(2048)
                    search_fin = re.search(r"\d*.bytes.*\/sec\)",result.decode("utf-8"))
                    if(search_fin):
                        print(switchIP + " Backup successful")
                        flag = False
                    search_fail = re.search(r".*Error opening.*.\(Timed out\)", result.decode("utf-8"))
                    if(search_fail):
                        print("Switch ip: %s tftp Server(%s) Timed out" % (switchIP, tftpSeverIP))
                        flag = False
                flagX = False
                break
            if(result_pwd):
                cmd.send(enPassword + "\n")
            if(result_enPwdErr):
                print("EXEC Mode password error")
                flagX = False
                break
        cmd.close()
        trans.close()

    except paramiko.ssh_exception.AuthenticationException:
        print("Login failed")
    except paramiko.ssh_exception.SSHException:
        print("connection timeout")
    