import helpers as h
import mysql.connector as con
import csv
import os
import math

DB_NAME = "knitITDatabase"
USER = "root"
PASSWORD = "root"
HOST = "127.0.0.1"

cnx = con.connect(user = USER, password = PASSWORD,  host = HOST, database = DB_NAME)
cursor = cnx.cursor()
garmentInsertString = h.buildInsertString("Garment", ("Name","GarmentTypeID", "YarnTestHeight", "YarnTestWidth", "YarnTestWeight"))
GarmentConstructionInsertString = h.buildInsertString("GarmentConstruction", ("GarmentID", "ConstructionID", "Measurements"))
print(garmentInsertString)

def mainMenu():
    print("What would you like to do?")
    print("(1) Design garment")
    print("(2) view garments")
    print("(0) Quit")

    answer = askForNumber("", 0,2)
    if answer == 0:
        return False
    if answer == 1:
        newGarment()
    if answer == 2:
        viewGarments()
    return True


def newGarment():

    cursor.execute("SELECT name, numberofparts, id FROM partspertype")

    garmentTypes = cursor.fetchall()

    i = 1
    for thing in garmentTypes:
        print(f"({i}) {thing[0]}, parts required: {thing[1]}")
        i += 1
    print("(0) Main menu")
    
    choice = askForNumber("What would you like to make? ", 0, len(garmentTypes))-1

    if choice == -1:
        return
    
    garmentType = garmentTypes[choice][2]
    constructions = askForConstructions(garmentType)

    print("Please use your chosen yarn and needles.\nCast on 10 stitches, knit 10 rows in stockinet stitch")
    yarnTestWidth = askForFloat("What is the width of your test square (cm)? ")
    yarnTestHeight = askForFloat("What ist the height of your test square (cm)? ")
    yarnTestWeight = askForFloat("What ist the weight of your test square (g)? ")

    name = input("What do you call your design? ")
    cursor.execute(garmentInsertString, (name, garmentType, yarnTestHeight, yarnTestWidth, yarnTestWeight))
    garmentId = cursor.lastrowid
    for thing in constructions:
        cursor.execute(GarmentConstructionInsertString,(garmentId, thing[0], thing[1]))
    cnx.commit()

def viewGarments():
    cursor.execute("SELECT g.id, g.name, gt.name "
    "FROM garment AS g "
    "JOIN garmenttype AS gt ON gt.id = g.garmenttypeid")

    existingGarments = cursor.fetchall()
    i = 1
    for thing in existingGarments:
        print(f"({i}) {thing[1]}: {thing[2]}")
        i += 1
    print("(0) Main menu")

    answer = askForNumber("", 0, len(existingGarments))-1

    if answer == -1:
        return

    cursor.execute("SELECT instructions "
    "FROM instructionsinorder "
    "WHERE id = %s "
    "order by priority", (existingGarments[answer][0],))

    instructions = cursor.fetchall()
    for thing in instructions:
        print(thing[0])
    

    0
def askForConstructions(garmentTypeId):

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

        print(f"Chose a type of {part[0]}:")

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

def askForFloat(message):
    number = input(message)
    try:
        float(number)
    except ValueError:
        print("Your answer should be a decimal number")
        number = askForFloat(message)
    return number

def yesNoQuestion(message):
    answer = input(f"{message} Y/N: ")
    answer = answer.lower()

    if answer != "y" and answer != "n":
        print("Please answer 'Y' or 'N'")
        answer = yesNoQuestion(message)
    return answer
    

keepGoing = True

while keepGoing:
    keepGoing = mainMenu()