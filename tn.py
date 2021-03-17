#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek.S
# FILE: tn.py
# DATE: 2021/03/17
# TIME: 10:56:37

# DESCRIPTION: telnet connect to Switch and backup config to tftp

import telnetlib

def tnBackup(switchIP, username, password, enPassword, tftpSeverIP):
    
    try:
        tn = telnetlib.Telnet(host=switchIP, port=23, timeout=10)
    except Exception as e:
        print("Can't connection %s" % switchIP)
    try:
        tn.read_until(b"Username:", timeout=5)
        tn.write(username.encode("ascii") + b"\n")
        tn.read_until(b"Password:", timeout=5)
        tn.write(password.encode("ascii") + b"\n")
        result = tn.expect([b"% Login invalid", b">"])
        if(result[0] == 0):
            print("Switch ip: %s Login password error" % switchIP)
        elif(result[0] == 1):
            tn.write(b"en\n")
            tn.read_until(b"Password:", timeout=5)
            tn.write(enPassword.encode("ascii") + b"\n")
            result = tn.expect([b"Password", b"% Bad secrets", b"#"])
            if(result[0] == 0):
                flag = True
                while(flag):
                    tn.write(enPassword.encode("ascii") + b"\n")
                    result = tn.expect([b"Password", b"% Bad secrets", b"#"])
                    if(result[0] == 1):
                        print("EXEC Mode password error")
                        flag = False
                        break
            elif(result[0] == 2):
                tn.read_until(b"#", timeout=5)
                tn.write(b"copy running-config tftp:\n")
                tn.write(tftpSeverIP.encode("ascii") + b"\n")
                tn.write(switchIP.encode("ascii") + b"\n")
                result = tn.expect([br".*%Error opening.*.\(Timed out\)", br"\d*.bytes.*\/sec\)"])
                if(result[0] == 0):
                    print("Switch ip: %s tftp Server(%s) Timed out" % (switchIP, tftpSeverIP))
                elif(result[0] == 1):
                    print(switchIP + " Backup successful")
                else:
                    print("Error")
        tn.close()

    except Exception as e:
        print(e)