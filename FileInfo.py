from Utils import *
import datetime
from colorama import Fore, Back, Style
from FIDlib_GTL import *

class FileEntry():

    def __init__(self,origFName, fid, metaPathID,  entry):
      self.fname = entry.name
      self.OriginalFileName = origFName
      self.MetaPathID = metaPathID
      self.FID = fid
      self.info = entry.stat()
      self.modDateTime = self.info.st_mtime
      self.lastAccessDateTime = self.info.st_atime
      self.fileSize = str(self.info.st_size)
      self.creationDateTime = self.info.st_ctime
      self.currentPath = os.path.dirname(entry.path)
      self.currentDrive  = ""
      self.fname2, self.fnameExtension=os.path.splitext(entry.path)
      self.fnameExtension=self.fnameExtension.strip(".")  #this is the extension that is written to the DB
      self.baseName, self.fileExtension = os.path.splitext(self.fname)
      self.fileExtension=self.fileExtension.strip(".") # . is still inserted into DB
      self.comment = ""
      self.withFID = AddFID(entry.name,self.FID)
      self.extractedFID = str(ExtractFID(self.withFID))
      self.fullPath = entry.path
      if self.creationDateTime>0:
        self.strCreationDateTime = str(datetime.datetime.fromtimestamp(self.creationDateTime))
        self.strCreationDate = str(datetime.date.fromtimestamp(self.creationDateTime))
        self.strModificationDateTime = str(datetime.datetime.fromtimestamp(self.modDateTime))
        self.strModificationDate = str(datetime.date.fromtimestamp(self.modDateTime))
      else:
        print(Fore.RED+"Error ---> Creation Date: "+str(self.creationDateTime)+Fore.WHITE)
        WriteToLog(r"c:\LogFiles\Log_IngestErrors.txt","Warning - Ingested with incorrect Creation Date ---> Creation Date: "+str(self.creationDateTime)+"   File Name: "+self.fname+"\t Path: "+self.currentPath)
        self.CreationDateTime = 0.0 

#
#   the .is_file test should likely be moved up to include all of the setup associated with the 'entry' parameter.
#   Also these may be a good place to look for the os.stat message source
#
      # if entry.is_file():
      #      print(Fore.LIGHTGREEN_EX+"\n\n<><><><><><><><> Class FileEntry <><><><><><><><><><>\n"+Fore.WHITE,self.info)
          #  print("             File Name: ", self.fname)
          #  print("             File Path: ", self.currentPath)
          #  print("File Without Extension: ", self.baseName)
          #  print("        File Extension: ", self.fnameExtension)
          #  print("             FName+FID: ", self.withFID)
          #  print("         extracted FID: ", self.extractedFID)
          #  print("    File Size in Bytes: ", self.fileSize)
          #  print("     Creation DateTime: ", datetime.datetime.fromtimestamp(self.creationDateTime))
          #  print("         Creation Date: ", datetime.date.fromtimestamp(self.creationDateTime))       
          #  print("       Access DateTime: ", datetime.datetime.fromtimestamp(self.lastAccessDateTime))
          #  print("           Access Date: ", datetime.date.fromtimestamp(self.lastAccessDateTime))
          #  print(" Modification DateTime: ", datetime.datetime.fromtimestamp(self.modDateTime))
          #  print("     Modification Date: ", datetime.date.fromtimestamp(self.modDateTime))
          #  print("              FullPath: ", self.fullPath)
          #  print(self.withFID)
          #  print("HasFID: "+str(HasFID(self.withFID)))
          #  RemoveFID(self.withFID)