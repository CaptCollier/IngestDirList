from SqlSrvr import SQL_AddFileInfo
import sys
import os
import datetime
from colorama import Fore, Back, Style
from Utils import *
from FileInfo import FileEntry
from FIDlib_GTL import *


metaPath=""
MetaPathID=""
drvLetter=r"R:"
curDrive="Drv_04"

#outFile = open("ExportFile.txt","a")


def InIgnoreList(inFileName):
    itemInIgnoreList=False
    for term in ignoreList:
           if term in inFileName:   
             itemInIgnoreList=True
    return itemInIgnoreList



print (Fore.GREEN+"[Starting Run]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+Fore.WHITE)

#MetaPathDictionary = Build2ElementDictionay('MetaPaths_Drv_04.txt')
#MetaPathDictionary = Build2ElementDictionay('MetaPaths_ForFileProcessing.txt')
foldersToProcessFile=input(Fore.YELLOW+"Filename containing pathnames to proces: "+Fore.WHITE)
MetaPathDictionary = Build2ElementDictionay(foldersToProcessFile)



ignoreList=readTextIgnorListToList(r'IgnoreList_File.txt')
PrintList(ignoreList)


for key,value in MetaPathDictionary.items():
        MetaPathID = key
        metaPath = value
        path =drvLetter+metaPath
        print (Fore.BLUE+ '\n\n\n>>>>>>>>>>>>>>>>>>>  Preparing to read Directory: ',path+"\n\n"+Fore.WHITE)
        dirContents = os.scandir(path)
        os.chdir(path)
        for entry in dirContents:
            if entry.is_file():
                #print(Fore.RED+"\n\n\n======================= Next File =========================")
                myFileEntry=FileEntry("",str(00000),MetaPathID,entry)
                myFileEntry.currentPath=metaPath
                myFileEntry.currentDrive=curDrive
                if not InIgnoreList(myFileEntry.fname):
                    if HasFID(myFileEntry.fname):
                        print(Fore.RED+"\n============== File Name Already Has FID ==========> "+myFileEntry.fname+"\n"+Fore.WHITE)
                        print(Fore.RED+ myFileEntry.currentPath +"\n"+Fore.WHITE)
                        WriteToLog(r"c:\LogFiles\Log_AlreadyHasFID.txt",myFileEntry.fname+","+ myFileEntry.currentPath) 
                    else:
                        myFileEntry.FID=SQL_AddFileInfo(myFileEntry)
                        myFileEntry.withFID=AddFID(myFileEntry.fname,str(myFileEntry.FID))
                        origFName = ConstructFullPath(myFileEntry.currentPath,myFileEntry.fname)
                        newFname  = ConstructFullPath(myFileEntry.currentPath,myFileEntry.withFID)
                        #print("Original File Name ---> "+origFName)
                        #print("New Filename with FID ====> " + newFname)
                        RenameFile(origFName,newFname)
                else:
                    print(Fore.RED+"\n============== File Name Is in ignore list ==========> "+myFileEntry.fname+Fore.WHITE)
                    WriteToLog(r"c:\LogFiles\Log_IgnoredFile.txt",myFileEntry.fname) 
            else:
                print(Fore.YELLOW+'\n!000000000000000000000 '+entry.name+' Is not a file 000000000000000000000000000000000')
                print("Is File: "+str(entry.is_file()))
                print("Is Dir: "+str(entry.is_dir())+Fore.WHITE)
