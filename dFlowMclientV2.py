import csv
from datetime import datetime,timedelta
from dateutil import parser
from tools import confreader,removeOldRecords
workDictFile= ".\\work\\dFlowDictV2.csv"
checkInterval=15
#####################################
def readDictFromCsv(file):

    with open(file,mode='r') as csv_file:
        reader = csv.reader(csv_file )

        mydict = {rows[0]: rows[1] for rows in reader}

        return mydict
    ################################################
def getTagByPath(path,config):

   for k in range(len(config.pointTag)):
      # print(config.directory[k])
       if config.directory[k] in path: return config.pointTag[k]
   return print ("cannot find : ",dir)
########################################################
def getDataFlowDict():
    print ("start remove old rec")
    removeOldRecords(workDictFile)
    print ("end remove old rec")
#p1
    watchDict= readDictFromCsv(workDictFile)
  #  print ("watchdict  ", watchDict)
    now= datetime.now()
    print(now)
    delta= timedelta(minutes=checkInterval)
    t1= now-delta
    t1s= str(t1)
    #p2
    config= confreader()
    operDict= dict()
    for tag in config.pointTag:
        operDict[tag]=[]
#p3
    for key in watchDict.keys():
        keyArr= key.split("@")
        time= keyArr[0]
        tag=keyArr[1]

        #p4
        timedt= parser.parse(time)

        if   now-delta < timedt <= now:

            eventtype=watchDict[key]
            operDict[tag].append( eventtype)
            if tag == "lgn01": print (key)
        #    operList.append(watchDict[key])
    status="novalue"
    resultDict=dict()
    for tag in operDict.keys():
      operList= set(operDict[tag])
      print (f"operlist for {tag}\n",operList)
      if 'deleted' in operList  and 'created' in operList :resultDict[tag]= "run"
      elif 'created' in operList:resultDict[tag] = "jam"
      else: resultDict[tag] = "nodata"
    print (resultDict)
    return resultDict
#getDataFlowDict()