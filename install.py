import mysql.connector as con
import csv
import os
import math

DB_NAME = "knitITDatabase"
USER = "root"
PASSWORD = "root"
HOST = "127.0.0.1"
startOfFilePath = os.getcwd() + "/Data/"  ##This is supposed to be everything that comes before "name.csv" in the Data file paths

def create_database(name, cursor):
    try:
        cursor.execute(f"CREATE DATABASE {name} DEFAULT CHARACTER SET 'utf8'")
    except con.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def insertCSVtoTable(nameOfTable, fileReader, insertString, dataTypesList, cursor):
    
    #This function itterates over every line in row in the csv reader. 
    #To use it you must send in a filereader where you already picked out the first row,
    #the one containing the names of the columns.

    for attributeList in fileReader:

        try:
            cursor.execute(insertString, attributeList)

        except con.Error as err:
            print(err)
        
def buildInsertString(tableName, attributeList):

    #Builds a string with the propper mqtt syntax to insert data in to a table

    numberOfAttributes = len(attributeList)
    return "INSERT INTO " +  tableName + "(" + ", ".join(attributeList) + ") " + "VALUES (" + "%s, "*(numberOfAttributes-1) + "%s)"

def buildTableInitiatingString(name, nameItterator, listOfDatatypes, primaryKey):

    #Builds a string with the proper mqtt syntax to initiate a new table in a database
    #Doing string concatination like this is slow but I dont care at the moment as It wil not be used many times

    tableString = f"CREATE TABLE `{name}` (" 
    i = 0
    for name in nameItterator:
        tableString += f"`{name}` {listOfDatatypes[i]}, "
        i += 1
    tableString += f"PRIMARY KEY (`{primaryKey}`))"
    return tableString




