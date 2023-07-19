import ftplib
import os
from collections import namedtuple
import time

session = namedtuple("session","ip port user psw")
def sendFolderFiles(session, filesFolderPath):

   # upFolderPath = upfolder[i]
    #     print("prepare list for ftp, path :", tempFolderPath)
    numsent = 0
    for name in os.listdir(filesFolderPath):
        fileLocalpath = os.path.join(filesFolderPath, name)
        if os.path.isfile(fileLocalpath):
            try:
                push_file_FTP(session.ip,session.port,session.user, session.psw,fileLocalpath)

                numsent = numsent + 1
                time.sleep(0.03)
                Remove1File(fileLocalpath)
            except ftplib.all_errors as e:
                numsent=-0.1
                break

        else:
            print("main, 208.1,source content error")

    return numsent
#=======================================================================
def Remove1File(localpath):
    print("Sending OK.system is removing :", localpath)

    try:

        os.remove(localpath)



    except OSError:
            print("file not found err")
            pass
    except PermissionError as es:
        print("exception point 102030")
    return
##################################################


def push_file_FTP(ip,port,user, psw,filePath):
    ftp = ftplib.FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    fileNameStrArr=str(filePath).split("\\")
    lastIndx= len(fileNameStrArr)-1
    fileName= fileNameStrArr[lastIndx]

    ftp.storbinary('STOR ' + fileName, open(filePath, 'rb'))
    ftp.close()