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

    #actionList = commaWithSpace("action.dat")
    #arc.dat: Needed for Province Game
    #backdoor.dat: Scenario
    #ccList = commaOnly("cc_tab.dat") Character Combat Chart is static and not needing of DB
    charList = commaOnly("charactr.dat")
    #detectList = commaOnly("detect.dat") Detection Chart is static
    #distance.dat: Needed for Province Game
    #egrix.dat: Scenario
    environList = commaOnly("environ.dat")
    #galactic.dat: Scenario
    #galevent.dat: Needed for Galactic Game
    #guistar.dat: Scenario file. Necessary?
    #helsinki.dat: Scenario
    #lookup.dat: Needed for Galactic Game.
    #milCombatList = commaOnly("milcomb.dat") Military Combat Chart is static
    #orlog.dat: Scenario
    #path.dat: Need key, no idea.
    planetList = commaOnly("planet.dat")
    possessionList = commaWithSpace("possessn.dat")
    #possimg.dat: Discuss. Need to be stored for Client?
    raceList = raceSnag("races.dat")
    #sov_hnd.dat: Need key, not star system, used by Environ
    spaceshipList = commaOnly("spacship.dat")
    #strategy.dat: Galactic Game
    #varu.dat: Scenario


    session = Session()  
    Base.metadata.create_all(db)    #Create the database.
  
    i = 1
    
    #The following for loops load up the database with relevant info pulled from the .dat files.
    
    
    for list in charList:
        temp = Character(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], 
                          list[8], list[9], list[10], list[11], list[12])
        session.add(temp)
    session.commit()
    
    
    for list in environList:
        if list[8] > 3:
            temp = Environ(list[0], list[1], list[2], list[3], list[4], 
                           list[5], list[6], list[7], -1, list[8],int(list[0])/10)
        else:
            temp = Environ(list[0], list[1], list[2], list[3], list[4], 
                           list[5], list[6], list[7], list[8], -1,int(list[0])/10)
        session.add(temp)
    session.commit()
    i = 1
    
    
    for list in planetList:
        temp = Planet(list[0], list[1], list[2], list[3], list[5])
        session.add(temp)
        # Implementing Orbit Boxes as Environ # 0 for each planet
        temp = Environ(list[0]+'0', 'O', '50', None, '0', '0', '0', 'None', '0', '0', list[0])
        session.add(temp)
    session.commit()
    
    for list in possessionList:
        if len(list) == 2:
            continue
        elif len(list) == 4:
            temp = Possession(list[0], list[1], list[2], list[3], " ", " ", " ", " ")
        elif len(list) == 5:
            temp = Possession(list[0], list[1], list[2], list[3], list[4], " ", " ", " ")
        elif len(list) == 6:
            temp = Possession(list[0], list[1], list[2], list[3], list[4], list[5], " ", " ")
        elif len(list) == 7:
            temp = Possession(list[0], list[1], list[2], list[3], list[4], list[5], list[6], " ")
        session.add(temp)


    for list in raceList:
        if list[4] == '*':
            temp = Race(list[0], list[1], list[2], list[3], False)
        else:
            temp = Race(list[0], list[1], list[2], list[3], True)
        session.add(temp)
    session.commit()

# Test data for Stack manipulation and others

    temp = Stack(3111)
    temp.characters = [ session.query(Character).filter_by(name = 'Adam Starlight').one(),
                        session.query(Character).filter_by(name = 'Zina Adora').one()]
    session.add(temp)
    temp = Stack(3111)
    temp.characters = [ session.query(Character).filter_by(name = 'Senator Dermond').one()]
    session.add(temp)
    session.commit()