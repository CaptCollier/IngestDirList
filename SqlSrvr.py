import pandas as pd
import pyodbc 
import datetime
from colorama import Fore, Back, Style
from FileInfo import FileEntry


###########################################################################################################
#
#  Create and return a DB Connection
#
###########################################################################################################
def SQL_FetchConnection():
    #
    # Create Connection
    #
    server = r'SNOWCRASH\SQLSERVER2017STD' 
    database = 'GTL' 
    username = 'scollier' 
    password = 'ranger' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password,autocommit=True)
    return cnxn


###########################################################################################################
#
# Execute a single SQL command passed in as a string, along with the connection for the DB
#
###########################################################################################################
def SQL_Execute(InCnXn, inCmd ):
    #
    #  Use Pandas to load the file for validation
    #
    sqlQueryResultSet = pd.read_sql(inCmd, InCnXn)
    return sqlQueryResultSet


###########################################################################################################
#
# Given a connection and a table name, dump the contents of the table to the terminal
#
###########################################################################################################
def SQL_DisplayTable(InCnXn, inTable):

    #
    #  Use Pandas to load the file for validation
    #
    sqlQueryResultSet=SQL_Execute(InCnXn,'Select * from ' + inTable +'')
    print (sqlQueryResultSet)
    return sqlQueryResultSet


###########################################################################################################
#
# Given a connection and a table name, dump the contents of the table to the terminal
#
###########################################################################################################
def SQL_DisplayTableOrderBy(InCnXn, inTable,inOrderByCol):

    #
    #  Use Pandas to load the file for validation
    #
    sqlQueryResultSet=SQL_Execute(InCnXn,'Select * from ' + inTable + ' order by '+inOrderByCol+' desc')
    print (sqlQueryResultSet)
    return sqlQueryResultSet


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////                                                         ////////////////////////////////
#///////////////////////////////////                  File Table PRocedures                  ////////////////////////////////
#///////////////////////////////////                                                         ////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

###########################################################################################################
#
# Insert information associated with a given file into the DB as an initial entry, returns the File ID
#
###########################################################################################################
def SQL_AddFileRec(localMetaPath,localOrigFileName,localFileExt,localCurrentFName,localCreateionDateTime,localCreationDate,localModDateTime,localModeDate,localSize,localCurrentDrv,localCurrentPath,localComments):
    inFID =0
    #print(Fore.LIGHTGREEN_EX+ "\n\n========================================================================================================\n\n"+Fore.WHITE)
    #
    # Fetch Connection
    #
    cnxn=SQL_FetchConnection()

    #
    #  Set up the procedure call
    #
    
    sql='exec uspNewFile_FID ?,?,?,?,?,?,?,?,?,?,?,?, ? OUTPUT'
    cursor=cnxn.cursor()
    values=(localMetaPath,localOrigFileName,localFileExt,localCurrentFName,localCreateionDateTime,localCreationDate,localModDateTime,localModeDate,localSize,localCurrentDrv,localCurrentPath,localComments,inFID)
    
    #
    # Perform the procedure call
    #
    try:
      inFID = int(cnxn.execute(sql,values).fetchone()[0])
    except pyodbc.Error as e: 
      print(Fore.RED+"SOC-AddFile pyodbc error: ",str(e)+Fore.WHITE)    
    #
    # close the connection
    #
    cnxn.close()
    return inFID


###########################################################################################################
#
# Insert information associated with a given file into the DB as an initial entry, returns the File ID
#
###########################################################################################################
def SQL_AddFileInfo(inFileInfo):
  localCurrentDrv        = inFileInfo.currentDrive
  localCurrentPath       = inFileInfo.currentPath
  localMetaPath          = inFileInfo.currentPath
  localMetaPathID        = int(inFileInfo.MetaPathID)
  localOrigFileName      = inFileInfo.baseName
  localCurrentFName      = inFileInfo.fname
  localFileExt           = inFileInfo.fnameExtension
  localSize              = int(inFileInfo.fileSize)

  if inFileInfo.creationDateTime>0:
    localCreationDateTime = datetime.datetime.fromtimestamp(inFileInfo.creationDateTime)
    localCreationDate      = datetime.date.fromtimestamp(inFileInfo.creationDateTime)
  else:
    localCreationDateTime="0001-01-01 00:00:00"
    localCreationDate="0001-01-01"

  
  localModDateTime       = datetime.datetime.fromtimestamp(inFileInfo.modDateTime)
  localModeDate          = datetime.date.fromtimestamp(inFileInfo.modDateTime)
  localComments          = inFileInfo.comment
  # print("\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  called AddFileINfo " )
  # print("        Current Drive: ", localCurrentDrv)
  # print("            File Path: ", localCurrentPath)
  # print("             MetaPath: ", localMetaPath)
  # print("          MetaPath ID: ", localMetaPathID)
  # print("   Original File Name: ", localOrigFileName)
  # print("       File Extension: ", localFileExt)
  # print("    Current File Name: ", localCurrentFName)
  # print("   File Size in Bytes: ", localSize)
  # print("    Creation DateTime: ", localCreationDateTime)
  # print("        Creation Date: ", localCreationDate) 
  # print("Modification DateTime: ", localModDateTime)     
  # print("    Modification Date: ", localModeDate) 
  # print("             Comments: ", localComments)
  newFID=SQL_AddFileRec(localMetaPathID,localOrigFileName,localFileExt,localCurrentFName,localCreationDateTime,localCreationDate,localModDateTime,localModeDate,localSize,localCurrentDrv,localCurrentPath,localComments)
  return newFID

###########################################################################################################
#
# Update a File record in the DB based on the FID.  Also passed in are the name of the Col to be updated
# and the new value.
#
###########################################################################################################
def SQL_UpdFileRec(inFID,inColName,inColValue):
    print(Fore.YELLOW + "\n\n========================================================================================================\n\n"+Fore.WHITE)
    #
    # Fetch Connection
    #
    cnxn=SQL_FetchConnection()
    #
    #  Set up the procedure call
    #
    sql='exec uspUPDFile ?,?,?'
    cursor=cnxn.cursor()
    values=(inFID,inColName,inColValue)
    #
    # Perform the procedure call
    #
    try:
      cnxn.execute(sql,values)
    except pyodbc.Error as e: 
      print("SOC-UpdFile pyodbc error: ",str(e))
    #
    # close the connection
    #
    cnxn.close()



###########################################################################################################
#
#  Fetch a File entry from the DB based on the FID
#
###########################################################################################################
def SQL_FetchFileRec(inFID):
    #
    # Fetch Connection
    #
    cnxn=SQL_FetchConnection()
    #
    #  Set up the procedure call
    #
    sql='exec uspFetchlFileByFID ?'
    cursor=cnxn.cursor()
    values=(inFID)
    #
    # Perform the procedure call
    #
    try:
      resultSet=cnxn.execute(sql,values)
      row=resultSet.fetchone()

    except pyodbc.Error as e: 
      print("SOC-FetchFileRec pyodbc error: ",str(e))
    #
    # close the connection
    #
    cnxn.close()
    return row    




###########################################################################################################
#
#  Delete a File entry from the DB based on the FID
#
###########################################################################################################
def SQL_DelFileRec(inFID):
    #
    # Fetch Connection
    #
    cnxn=SQL_FetchConnection()
    #
    #  Set up the procedure call
    #
    sql='exec uspDelFileByFID ?'
    cursor=cnxn.cursor()
    values=(inFID)
    #
    # Perform the procedure call
    #
    try:
      cnxn.execute(sql,values)
    except pyodbc.Error as e: 
      print("SOC-DelFileRec pyodbc error: ",str(e))
    #
    # close the connection
    #
    cnxn.close()



#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////                                                         ////////////////////////////////
#///////////////////////////////////                  MetaPath PRocedures                    ////////////////////////////////
#///////////////////////////////////                                                         ////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

###########################################################################################################
#
# Insert information associated with a given MetaPath into the DB as an initial entry, returns the MetaPath ID
#
###########################################################################################################
def SQL_AddMetaPathRec(localDrive, localMetaPath, localStatus, localComments):
    inMetaPathID =0
    #print(Fore.LIGHTGREEN_EX+ "\n\n========================================================================================================\n\n"+Fore.WHITE)
    #
    # Fecht Connection
    #
    cnxn=SQL_FetchConnection()
    #
    #  Set up the procedure call
    #
    sql='exec uspNewMetaPath_ID ?,?,?,?, ? OUTPUT'
    cursor=cnxn.cursor()
    values=(localDrive, localMetaPath, localStatus, localComments, inMetaPathID)
    #
    # Perform the procedure call
    #
    try:
      inMetaPathID = int(cnxn.execute(sql,values).fetchone()[0])
     # print("Call executed Returned new MetaPath_ID: ",inMetaPathID)
    except pyodbc.Error as e: 
      print("SOC-AddMetaPath pyodbc error: ",str(e))
    #
    # close the connection
    #
    cnxn.close()
    return inMetaPathID


###########################################################################################################
#
#  Fetch a MetaPath entry from the DB based on the MetaPathID
#
###########################################################################################################
def SQL_FetchMetaPathRec(inMetaPathID):
    #
    # Fetch Connection
    #
    cnxn=SQL_FetchConnection()
    #
    #  Set up the procedure call
    #
    sql='exec uspFetchMetaPathRecByID ?'
    cursor=cnxn.cursor()
    values=(inMetaPathID)
    #
    # Perform the procedure call
    #
    try:
      resultSet=cnxn.execute(sql,values)
      # print(resultSet)
      row=resultSet.fetchone()
      # print("Row: ",row)
      # print("MetaPathID: ",row[0])
      # print("     Drive: ",row[1])
      # print("  MetaPath: ",row[2])
      # print("    Status: ",row[3])
      # print("   Comment: ",row[4])
      # for item in row:
      #   print(item)
    except pyodbc.Error as e: 
      print("SOC-FetchMetaPathRec pyodbc error: ",str(e))
    #
    # close the connection
    #
    cnxn.close()
    return row


###########################################################################################################
#
# Update a MetaPath record in the DB based on the MetaPathID.  Also passed in are the name of the Col to be updated
# and the new value.
#
###########################################################################################################
def SQL_UpdMetaPathRec(inMetaPathID,inColName,inColValue):
    #
    # Fetch Connection
    #
    cnxn=SQL_FetchConnection()
    #
    #  Set up the procedure call
    #
    sql='exec uspUpdMetaPath ?,?,?'
    cursor=cnxn.cursor()
    values=(inMetaPathID,inColName,inColValue)
    #
    # Perform the procedure call
    #
    try:
      cnxn.execute(sql,values)
    except pyodbc.Error as e: 
      print("SOC-uspUpdMetaPath pyodbc error: ",str(e))
    #
    # close the connection
    #
    cnxn.close()
  

###########################################################################################################
#
#  Delete a File entry from the DB based on the MetaPathID
#
###########################################################################################################
def SQL_DelMetaPathRec(inMetaPathID):
    #
    # Fetch Connection
    #
    cnxn=SQL_FetchConnection()
    #
    #  Set up the procedure call
    #
    sql='exec uspDelMetaPathByID ?'
    cursor=cnxn.cursor()
    values=(inMetaPathID)
    #
    # Perform the procedure call
    #
    try:
      cnxn.execute(sql,values)
    except pyodbc.Error as e: 
      print("SOC-uspDelMetaPathByID pyodbc error: ",str(e))
    #
    # close the connection
    #
    cnxn.close()


