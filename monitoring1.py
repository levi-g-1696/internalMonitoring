import csv
import datetime
import os
import random
import string
import time
from collections import namedtuple
from checkFunctions import isAppInRunnigList, checkPyApp,checkSQLconnection,checkErmApnNetwork
from sendFile import session, sendFolderFiles
import pyodbc as pyodbc

config = namedtuple("config", "checkFunc appName tag cmdString argString")
configFile= ".\\config2.csv"
serverTag= "LGNTsrv"
directory= r"D:\internal monitoring"
sqlTarget = "192.168.203.61,1433\\SQLEXPRESS"
sqlUser = "agr"
sqlPsw = '23@@enviRo'



##############   GET     ####################
def getHeadString():
    str= "TabularTag,DateTime"
    from checkFunctions import checkFuncDict
    for key in checkFuncDict:
        str = str + "," + key
   # conf = confreader(configFile)

    return str
#########################################################
def getValString(valDict):

    dt= datetime.datetime.now()
    dtstr= dt.isoformat()
    dtstr= dtstr.split(".")[0] #without second
    st= serverTag +","+ dtstr
    for key in valDict:
        st= st+ ','+ str(valDict[key])



    return st
################################################

######################################################################################
def getAppRunDictV7():

   from checkFunctions import checkFuncDict
   appRunDict=dict()
   for key in checkFuncDict:
       checkFunction= checkFuncDict[key]
       val = 1 if eval (checkFunction) else 0
       appRunDict[key] = val

   return appRunDict
############################################
def getStateFile():
    str1 = getHeadString()
    appRunDict = getAppRunDictV7()
    str2 = getValString(appRunDict)

    destfile = makeFileName("LGNTsrv", directory, datetime.datetime.now())
    with open(destfile, "a") as myfile:
        myfile.write(str1 + "\n")
        myfile.write(str2 + "\n")
    print(str2)
    print(f"server monitoring results are succesfuly stored to file {destfile}")

########################################  I  M   #############
# def isAppInRunnigList(cmd,arg):
#     output2 = os.popen('wmic process get commandline, description, processid').read()
#     processList = output2.split("\n")
#     print (processList)
#     found = False
#     for item in processList:
#         itemWithoutCmd= item.replace(cmd,'')
#         if cmd in item and (arg =="" or arg  in itemWithoutCmd):
#             found= True
#             item = item.replace("        "," ")
#             item = item.replace("        ", " ")
#             print (f"isAppInRunningList says:Success. {cmd} was found\n {item}")
#
#     return  found
#################################################

def apply(func, x, y):
       return func(x, y)
####################################

def makeFileName(stationName, destFolder, datetime):
    formatStr="H171120230100_171120230100_637-"
    zeroChar = ""
    if (datetime.month < 10): zeroChar = "0"
    fullFilePath = destFolder + "\\" + stationName + "."+formatStr + str(datetime.year) + zeroChar + str(datetime.month) + str(datetime.day) + "." + str(datetime.hour) + str(datetime.minute)
    randomStr = ''.join(random.choices(string.digits + string.ascii_letters, k=5))
    fullFilePath = fullFilePath + "-" + randomStr + ".csv"
    return fullFilePath
#######################################################
if __name__ == '__main__':
    for k in range(118):
      getStateFile()  # makes state file in "directory" folder
      monCenter = session("2.55.113.138", "21", "loggernet-srv", "23enviRo23")
      n = sendFolderFiles(monCenter, directory)
      print(f"server status file was succesfully sent to monitoring center: {n} files")
      time.sleep(59)