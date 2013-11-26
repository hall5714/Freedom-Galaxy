#Author: Greg Donaldson
#Revisions: Jeff Crocker
#Purpose: Created for the purpose of pulling data from the .dat files for Freedom in the Galaxy. 
#Primarily for use by the backend team. This will allow for a database to be used.

#os is needed to make sure we don't connect to a pre-existing database.
#The others are for creating the database.

import os
from sqlalchemy import *
from dataSnag import *
from orm import *

import re

def data_parser(file_name):
    """
    For given file_name, parse lines into a list of lists of data.

    Uses the regular expression '[A-Z0-9/ "'*.\-]+' to capture
    groups of data; ignores empty lines and those starting with '#'

    Regular expression explanation: [] indicates a character set, with
    the +, it matches any string consisting of one or more of those
    characters. Using the IGNORECASE flag, we need only specify the
    alphabet by the range A-Z, the digits 0-9, forward slash, space,
    double quote, single quote, asterisk, period, and hyphen. Note
    that the last is the only one that needs to be escaped inside a
    character set. The expression is encapsulated by triple quotes to
    allow for easy inclusing of the quote characters, and is made
    'raw' with the r prefix, so that the backslash can be used
    literally. All these characters were founda as valid data in some
    data file.

    This function replaces those that were found in dataSnag.py

    """
    data_list = []
    regex = re.compile(r"""[A-Z0-9/ "'*.\-]+""", flags=re.IGNORECASE)
    with open(file_name) as data:
        for line in data:  # iterate over lines in the file
            if not line.strip().startswith('#') and line.strip():
            # not a comment and exists
                data_list.append([match.strip() for match in
                                  re.findall(regex, line)])
    return data_list

def loadDatabase():
    print "Loading database"

    #Alright, time to check if the database already exists. If it does, get rid of it. 
    #If it doesn't, don't.
    try:
        os.remove("Freedom.db")
        db = create_engine('sqlite:///Freedom.db')
    except:      
        db = create_engine('sqlite:///Freedom.db')


    #These are the lists returned by dataSnag's functions. Necessary for the database.

    #actionList = data_parser("action.dat")
    #arc.dat: Needed for Province Game
    #backdoor.dat: Scenario
    #ccList = data_parser("cc_tab.dat") Character Combat Chart is static and not needing of DB
    charList = data_parser("./dat_files/charactr.dat")
    #detectList = data_parser("detect.dat") Detection Chart is static
    #distance.dat: Needed for Province Game
    #egrix.dat: Scenario
    environList = data_parser("./dat_files/environ.dat")
    #galactic.dat: Scenario
    #galevent.dat: Needed for Galactic Game
    #guistar.dat: Scenario file. Necessary?
    #helsinki.dat: Scenario
    #lookup.dat: Needed for Galactic Game.
    #milCombatList = data_parser("milcomb.dat") Military Combat Chart is static
    milunitsList = data_parser("./dat_files/military_units.dat")
    #orlog.dat: Scenario
    #path.dat: Need key, no idea.
    planetList = data_parser("./dat_files/planet.dat")
    possessionList = data_parser("./dat_files/possessn.dat")
    #possimg.dat: Discuss. Need to be stored for Client?
    raceList = data_parser("./dat_files/races.dat")
    #sov_hnd.dat: Need key, not star system, used by Environ
    #spaceshipList = data_parser("spacship.dat")
    #strategy.dat: Galactic Game
    #varu.dat: Scenario


    session = Session()
    Base.metadata.create_all(db)    #Create the database.

    i = 1

    #The following for loops load up the database with relevant info pulled from the .dat files.
    for list in charList:
        temp = Characters(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], 
                          list[8], list[9], list[10], list[11], list[12])
        session.add(temp)
    #session.commit()


    for list in environList:
        if list[8] > 3:
            temp = Environs(list[0], list[1], list[2], list[3], list[4], 
                           list[5], list[6], list[7], -1, list[8],int(list[0])/10)
        else:
            temp = Environ(list[0], list[1], list[2], list[3], list[4], 
                           list[5], list[6], list[7], list[8], -1,int(list[0])/10)
        session.add(temp)
    session.commit()
    i = 1

    for list in milunitsList:
        temp = MilitaryUnits(list[0], list[1], list[2], list[3], list[4])
        session.add(temp)
    session.commit()

    for list in planetList:
        temp = Planets(list[0], list[1], list[2], list[3], list[5])
        session.add(temp)
        # Implementing Orbit Boxes as Environ # 0 for each planet
        temp = Environs(list[0]+'0', 'O', '50', None, '0', '0', '0', 'None', '0', '0', list[0])
        session.add(temp)
    session.commit()

    for list in possessionList:

        if len(list) == 2:
            continue
        elif len(list) == 4:
            temp = Possessions(list[0], list[1], list[2], list[3], " ", " ", " ", " ")
        elif len(list) == 5:
            temp = Possessions(list[0], list[1], list[2], list[3], list[4], " ", " ", " ")
        elif len(list) == 6:
            temp = Possessions(list[0], list[1], list[2], list[3], list[4], list[5], " ", " ")
        elif len(list) == 7:
            temp = Possessions(list[0], list[1], list[2], list[3], list[4], list[5], list[6], " ")
        session.add(temp)


    for list in raceList:
        if list[4] == '*':
            temp = Races(list[0], list[1], list[2], list[3], False)
        else:
            temp = Races(list[0], list[1], list[2], list[3], True)
        session.add(temp)
    session.commit()

# Test data for Stack manipulation and others

    temp = Stacks(3111)
    temp.characters = [ session.query(Characters).filter_by(name = 'Adam Starlight').one(),
                        session.query(Characters).filter_by(name = 'Zina Adora').one()]
    temp.characters[0].possessions = [ session.query(Possessions).filter_by(name
                                        = 'Star Cruiser').one()]
    #temp.characters[0].detected = True
    session.add(temp)
    temp = Stacks(3111)
    temp.characters = [ session.query(Characters).filter_by(name = 'Senator Dermond').one()]
    session.add(temp)
# More Test stacks.
#    temp = Stack(3112)
#    temp.militaryunits = [ session.query(MilitaryUnits).filter_by
#                         (side = 'Imperial', type = 'Militia'
    session.commit()
