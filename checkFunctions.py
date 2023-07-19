###############################
import pyodbc,datetime,os

checkFuncDict={
"mLGNT":"isAppInRunnigList(r'Campbellsci\LoggerNet')",
"mAmnon":"isAppInRunnigList(r'Send2Erm_new.exe')",
"mCR510": "checkPyApp(r'D:\Campbell-CR510\lastOperation.log',60)",
"mConSV": "checkPyApp(r'D:\Conditional Sync\py\lastRun.log',60)",
"mFZila": "isAppInRunnigList(r'FileZilla')",
"mSQL":"checkSQLconnection(sqlTarget,sqlUser,sqlPsw)",
"mErmApn":"checkErmApnNetwork()"
}

cmd=r'Campbellsci\LoggerNet'



def checkSQLconnection(target,user,psw):

    cnxn= pyodbc.connect(driver='{SQL Server Native Client 11.0}', server=target, database="agr-dcontrol", uid=user, pwd=psw)
    cursor = cnxn.cursor()
    try:
    #  print("execSelelect says:exequte sql query:\n", req)
      req= "SELECT top 1 * FROM INFORMATION_SCHEMA.TABLES"
      cursor.execute(req)
      rows = cursor.fetchall()
      return True
    except pyodbc.Error as ex:
      return False

#######################################################################################################
def checkPyApp(logFile,timeLimit):
    try:
      f = open(logFile, "r")
      line= f.readline()
      lineArr= line.split("=")
      lastRunCtime= int(lineArr[1])
      now = datetime.datetime.now().timestamp()
      if now - lastRunCtime < timeLimit :return True
      else: return False
    except Exception:
        print("cannot find last run log file: ", logFile)
        return False

    #############################################
def isAppInRunnigList(cmd):
        output2 = os.popen('wmic process get commandline, description, processid').read()
        processList = output2.split("\n")
       # print(processList)
        found = False
        for item in processList:
            if cmd in item :
                found = True
                item = item.replace("        ", " ")
                item = item.replace("        ", " ")
                print(f"isAppInRunningList says:Success. {cmd} was found\n {item}")
        return found
#############################################
def checkPing(hostname):

    response = os.system("ping -n 1 " + hostname)
    # and then check the response...
    if response == 0:
       return True
    else:
       return False
    ########################################
def checkErmApnNetwork() :
   ipList=["10.210.14.88","10.210.14.138","10.210.14.4","10.210.14.139","10.210.14.46","10.210.14.128","10.210.14.48"]
   res=False
   for ip in ipList:
       if checkPing(ip) :
           res= True
           break
   return res
