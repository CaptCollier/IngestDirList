import os
from colorama import Fore, Back, Style


def AddFID(inFileName,FID):
    baseName, fileExtension = os.path.splitext(inFileName)
    if not HasFID(baseName):
      outFName=baseName+"_FID-"+FID+fileExtension 
    else:
      outFName=inFileName
    return outFName

def ExtractFID(inFileName):
    FIDstartLoc=inFileName.find('_FID-')
    if (FIDstartLoc!=-1):
        FIDstartLoc+=5
        FIDendLoc=inFileName.rfind('.')
        outFID=inFileName[FIDstartLoc:FIDendLoc]
    else:
        outFID=-1
    return outFID

def HasFID(inFileName):
    # print("Procedure-HasFID inFileName: "+inFileName)
    fidPosition=inFileName.find('_FID-')
    # print("Starting Position of FID: "+str(fidPosition))
    if (fidPosition!=-1):
        FIDpresent=True
    else:
        FIDpresent=False
    # print("Has Fid: "+str(FIDpresent))
    return FIDpresent

def RemoveFID(inFileName):
    print("RemoveFID inFileName: "+inFileName)
    if HasFID(inFileName):
        FIDstr='_FID-'+ExtractFID(inFileName)
        outFileName=inFileName
        outFileName=outFileName.replace(FIDstr,"")
    else:
        outFileName=""
    print("Removing FID from ===="+inFileName+"  Resulting in Original File Name: "+outFileName)
    return outFileName



