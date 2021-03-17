import helpers as h
import mysql.connector as con
import csv
import os
import math

DB_NAME = "knitITDatabase"
USER = "root"
PASSWORD = "root"
HOST = "127.0.0.1"

def newGarment(cursor):
    garmentType = ""
    name = ""
    YarnTestHeight = ""
    YarnTestHeight = ""
    YarnTestWeight = ""

    cursor.execute("SELECT name, numberofparts, id FROM partspertype")

    garmentTypes = cursor.fetchall()

    i = 1
    for thing in garmentTypes:
        print(f"({i}) {thing[0]}, parts required: {thing[1]}")
        i += 1
    print("Quit (0)")
    
    choice = askForNumber("What would you like to do?", 0, len(garmentTypes))-1

    if choice == -1:
        return False
    
    garmentType = garmentTypes[choice][2]
    print(askForConstructions(garmentType, cursor))
    return True

def askForConstructions(garmentTypeId, cursor):
    choosenConstructions = []

    cursor.execute("SELECT p.name, gtp.partid, gtp.required FROM garmenttypepart AS gtp "
    "JOIN part AS p ON p.id = gtp.partid "
    "WHERE gtp.garmenttypeid = %s "
    "ORDER BY gtp.required", (garmentTypeId,))

    partsNeeded = cursor.fetchall()
    for part in partsNeeded:
        if part[2] == 0:
            answer = yesNoQuestion(f"Would you like to have a {part[0]}")
            if answer == "n":
                continue
        cursor.execute("SELECT name, id, measurementsneeded FROM construction "
                       "WHERE partid = %s", (part[1],)) 
        constructions = cursor.fetchall()
        print(constructions)
        print(f"Chose a type pf {part[0]}:")

        i = 1
        for thing in constructions:
            print(f"({i}) {thing[0]}")
            i += 1

        choice = askForNumber("Pick a construction: ", 1, len(constructions))-1
        choosenConstructions.append((constructions[choice][1], constructions[choice][2]))

    return choosenConstructions


def askForNumber(message, min, max):
    choice = input(message)

    if not choice.isdigit():
        print("Your choice must be a number")
        choice = askForNumber(message, min, max)
        

    choice = int(choice)

    if choice > max or choice < min:
        print("That choice is not available")
        choice = askForNumber(message, min, max)

    return choice

def yesNoQuestion(message):
    answer = input(f"{message} Y/N: ")
    answer = answer.lower()
    print(answer)
    if answer != "y" and answer != "n":
        print("Please answer 'Y' or 'N'")
        answer = yesNoQuestion(message)
    return answer
    



cnx = con.connect(user = USER, password = PASSWORD,  host = HOST, database = DB_NAME)
cursor = cnx.cursor()

keepGoing = True

while keepGoing:
    keepGoing = newGarment(cursor)