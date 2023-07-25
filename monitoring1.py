import csv
import datetime
import os
import random
import string
from dFlowMclientV2 import getDataFlowDict
import time
from collections import namedtuple
from checkFunctions import isAppInRunnigList, checkPyApp,checkSQLconnection,checkErmApnNetwork
from sendFile import session, sendFolderFiles
import pyodbc as pyodbc
from tools import readDictFromCsv,watchDictFile

config = namedtuple("config", "checkFunc appName tag cmdString argString")
configFile= ".\\configFunctonalityPoints.csv"
srvStatTag= "LGNTsrv"
srvDflowTag= "LgntDflow"
directory= r"D:\internal monitoring"
sqlTarget = "192.168.203.61,1433\\SQLEXPRESS"
sqlUser = "agr"
sqlPsw = '23@@enviRo'



##############   GET     ####################
def getSrvStateCsvHead():
    str= "TabularTag,DateTime"
    from checkFunctions import checkFuncDict
    for key in checkFuncDict:
        str = str + "," + key
   # conf = confreader(configFile)

    return str
#########################################################
def getValString(valDict,tag):

    dt= datetime.datetime.now()
    dtstr= dt.isoformat()
    dtstr= dtstr.split(".")[0] #without second
    st= tag + "," + dtstr
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
    str1 = getSrvStateCsvHead()
    appRunDict = getAppRunDictV7()
    str2 = getValString(appRunDict,srvStatTag)

    destfile = makeFileName("LGNTsrv", directory, datetime.datetime.now())
    with open(destfile, "a") as myfile:
        myfile.write(str1 + "\n")
        myfile.write(str2 + "\n")
    print(str2)
    print(f"server monitoring results are succesfuly stored to file {destfile}")

#################################################
def getDFlowFile():
    str1 = getDataFlowCsvHead(r"C:\Users\DownloadServer\PycharmProjects\internalMonitoring\configDataFlowPoints.csv")
    dFlowDict = getDataFlowDict()
 #   print (dFlowDict)
    str2 = getValString(dFlowDict,srvDflowTag)

    destfile = makeFileName(srvDflowTag, directory, datetime.datetime.now())
    with open(destfile, "a") as myfile:
        myfile.write(str1 + "\n")
        myfile.write(str2 + "\n")
    print (str1)
    print(str2)
    print(f"server data flow results are succesfuly stored to file {destfile}")

#################################################
def getDataFlowCsvHead(file):
    line = "TabularTag,DateTime"
    from tools import readDictFromCsv
    monlst=[]
    with open(file,mode='r') as csv_file:
        reader = csv.reader(csv_file )
        for rows in reader:
            monlst.append(rows[1])

    monlst.pop(0)   #remove header of column
    for m in  monlst:
        line = line + "," + m
    return line
###############################################
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
      getDFlowFile()
      monCenter = session("2.55.113.138", "21", "loggernet-srv", "23enviRo23")
      n = sendFolderFiles(monCenter, directory)
      print(f"server status file was succesfully sent to monitoring center: {n} files")
      time.sleep(59)


getDFlowFile()