import os
from colorama import Fore, Back, Style


def readTextIgnorListToList(inFile):
    print ("\nLoading File: "+inFile)
    ignoreList=[] 
    print("\nCreated the ignoreList in proc Length is: " + str(len(ignoreList))+"\n")
    inFile = open(inFile, "r")
    inLine = inFile.readline()
    inLine = inLine.replace("\n","") 
    ignoreList.append(inLine)
    while inLine: 
        inLine = inFile.readline()
        inLine = inLine.replace("\n","") 
        if (inLine != ""):
            ignoreList.append(inLine)
    inFile.close()
    print("\nJust Read the ignoreList Length is: " + str(len(ignoreList))+"\n")
    return ignoreList


def CsvStringToList(inString):
    li = list(inString.split(","))
    # print("splitting path into "+str(len(li))+" elements...")
    # print(*li, sep = ", ")
    # print("\n")
    return li

def CvsStringToListSkipFirst(inString):
    li = list(inString.split(","))
    # print("-->>Pre-splitting path into "+str(len(li))+" elements...")
    # print(*li, sep = ", ")
    # print("\n")
    #### this should delete the first item in the list check it out    li[1:]
    del li[0]
    # print("<<--Post-splitting path into "+str(len(li))+" elements...")
    # print(*li, sep = ", ")
    return li


def AppendListToFile(inList, elementOutFile):
    # print("====> Appending "+str(len(inList))+" elements to file "+elementOutFile+"...\n")
    # print(*inList, sep = ", ")
    with open(elementOutFile, 'a') as filehandle:
        filehandle.writelines("%s\n" % item for item in inList)
    # print(">==== Items Appended")

def PrintList(inList):
    print("\n")
    print("inListCount: " + str(len(inList))+"\n")
    for f in inList:
	    print(f)
    print("\n")


def RenameFile(oldFileName,newFileName):
    try:
      os.rename(oldFileName,newFileName)
    except:
      errorMessage="\n#--------------- File Not Found Error - Rename -------------------\n"
      errorMessage="Old: "+oldFileName  
      WriteToLog(r"c:\LogFiles\Log_FileNotFoundError.txt",errorMessage)
      errorMessage="New: "+newFileName  
      WriteToLog(r"c:\LogFiles\Log_FileNotFoundError.txt",errorMessage)
      print(Fore.RED+'\n!!!!!!!!!!!!!!!!!!!!!!  File Not Found Error - Rename !!!!!!!!!!!!!!!!!!!!!!!!!!!!')
      print("Original: "+oldFileName)
      print("     New: "+newFileName+Fore.WHITE)


def ConstructFullPath(inPath, inFileName):
     fullPath=inPath+"\\"+inFileName
     return fullPath

def BuildFullPath(inFileEntry):
     outFullPath= inFileEntry.fullPath
     return outFullPath

def ExportFileInfo(outFile, inFile):
    outLine = ('"'  +inFile.FID+
               '","'+inFile.MetaPathID+
               '","'+inFile.OriginalFileName+
               '","'+inFile.fnameExtension+
               '","'+inFile.fname+
                '","'+inFile.strCreationDateTime+
                '","'+inFile.strCreationDate+
                '","'+inFile.strModificationDateTime+
               '","'+inFile.strModificationDate+
               '","'+inFile.fileSize+
               '","'+inFile.currentPath+
               '","'+inFile.comment+'"\n')
    #print("outline to Export --> ",outLine)
    outFile.write(outLine)


def WriteToLog(inLogFile,inLine):
    outFile = open(inLogFile,"a")
    try:
      outFile.writelines(inLine+"\n")
    except:
      print(Fore.RED+"Error ---> Writing to log \n"+Fore.WHITE)
      outFile.writelines("Error ---> file Name Unknown - likely file has unprintable characters \n")

    outFile.close()



def Build2ElementDictionay(localInFile):
    print("Building 2 Element Dictionary")
    local_Dictionary = dict()
    inFile = open (localInFile,"r")
    inLine = inFile.readline()
    while inLine: 
       inLine = inLine.strip('\n')
       if inLine !="":
         try:
           (key, val) = inLine.split(",")
           local_Dictionary[key] = val
         except:
             WriteToLog("c:\LogFiles\Log_Build2DictionaryErrors.txt","Failed to Parse: "+inLine)
             print(Fore.RED+"Log_Build2DictionaryErrors.txt","---> Error Failed to Parse: "+inLine+Fore.WHITE)
       inLine = inFile.readline()
    inFile.close()
    #print(local_Dictionary)
    return local_Dictionary

def DumpKeyValuePair(localDictionary):
    for key,value in localDictionary.items():
        MetaPathID = key
        metaPath = value
        print("Key:Value    "+key+" : "+value)
    print("\n")
    
