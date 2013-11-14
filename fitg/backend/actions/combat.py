from database_creation import loadDatabase
from orm import *
from random import randint


def char_combat(AtkID, DefID, Options):

	session = Session()

	atk_stack = session.query(Stack).filter_by(id = AtkID).one()
	def_stack = session.query(Stack).filter_by(id = DefID).one()

	# still needs to include breakoff and capture modifiers
	# also decision if firefight or hand-to-hand

	CD = stack_combat_rating(AtkID, session) - stack_combat_rating(DefID, session)

	if 'C' in Options:
		CD -= 2

	atk_result = char_table(randint(0,5),CD,True)
	def_result = char_table(randint(0,5),CD,False)

	if 'F' in Options:
		atk_result[0] *= 2
	if atk_stack.militaryunits:
		atk_result[0] *= 2
		
	if 'C' in Options:
		if atk_result[1] == 1:
			CapturedChar = def_stack.characters[randint(0,len(def_stack.characters)-1)]
			CapturedChar.stack_id = AtkID
			CapturedChar.captive = True
			CapturedChar.active = False

		if def_result[1] == 1:
			CapturedChar = def_stack.characters[randint(0,len(def_stack.characters)-1)]
			CapturedChar.stack_id = AtkID
			CapturedChar.captive = True
			CapturedChar.active = False

	session.add(atk_stack, def_stack)
	session.commit()

def suffer_wounds(character, num, session):
	pass

def stack_combat_rating(StackID, session):
	CR = 0
	for character in session.query(Stack).filter_by(id = StackID).one().characters:
		if character.active == True:
			CR += character.combat - character.wounds
	return CR

def char_table(dice, CD, IsAttacker):
	AttackerWounds = (
		(4,3,3,2,2,2,2,1,1,1),(4,3,2,2,2,1,1,1,1,0),(3,3,2,2,1,1,1,1,0,0),
		(3,2,2,1,1,1,0,0,0,0),(2,2,1,1,0,0,0,0,0,0),(2,1,0,0,0,0,0,0,0,0))

	DefenderWounds = (
		(0,0,0,0,0,0,0,1,1,2),(0,0,0,0,0,0,1,1,1,2),(0,0,0,0,0,1,1,1,2,3),
		(0,0,0,1,1,1,1,2,3,3),(0,0,1,1,1,1,2,2,3,4),(1,1,1,1,2,2,2,3,3,4))

	AttackerCapture = (
		(0,0,0,0,0,1,0,0,0,0),(0,0,0,1,1,0,1,1,1,0),(0,1,0,0,0,0,0,0,0,0),
		(0,0,1,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,1,0,0),(0,0,0,0,0,0,0,0,0,0))

	DefenderCapture = (
		(0,0,0,0,0,0,0,0,1,0),(0,0,0,0,0,0,0,0,0,0),(0,0,0,0,1,0,0,1,1,0),
		(0,0,0,1,0,1,1,1,0,0),(0,0,0,0,0,0,1,0,1,0),(0,0,0,0,0,0,0,0,0,0))

	if IsAttacker:
		return (AttackerWounds[dice][CD], AttackerCapture[dice][CD])
	else:
		return (DefenderWounds[dice][CD], DefenderCapture[dice][CD])

#Authored By Ben Cumber
#military_units.dat info format
#side, type, mobility, environ combat, space combat
def mil_combat(atk_id, def_id):
    session = Session()

    atk_stack = session.query(Stack).filterby(id = atk_id).one()
    def_stack = session.query(Stack).filterby(id = def_id).one()

    atk_mil_units = atk_stack.militaryunits
    def_mil_units = def_stack.militaryunits


def mil_combat_table(die_roll, combat_odds, is_attacker):
    defender_wounds = (
            (8, 7, 6, 5, 5, 4, 3, 3, 2, 2, 1),
            (7, 6, 5, 5, 4, 3, 2, 2, 1, 1, 1),
            (7, 5, 5, 4, 3, 2, 2, 2, 1, 1, 1),
            (6, 5, 4, 3, 3, 2, 1, 1, 1, 0, 0),
            (5, 4, 4, 3, 2, 1, 1, 0, 0, 0, 0),
            (4, 4, 3, 3, 1, 0, 0, 0, 0, 0, 0))
    
    attacker_wounds = (
            (0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 4),
            (0, 0, 0, 0, 0, 1, 2, 3, 3, 4, 5),
            (0, 0, 0, 0, 1, 1, 2, 3, 4, 4, 5),
            (0, 0, 1, 1, 1, 2, 3, 3, 4, 5, 6),
            (1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7),
            (1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8))


if __name__ == "__main__":
    loadDatabase()

    session = Session()
    print session.query(Stack).filter_by(id = 1).one().characters
    print "Before:"
    for character in session.query(Stack).filter_by(id = 1).one().characters:
            print character
    char_combat(2,1,'C')
    print "After:"
    for character in session.query(Stack).filter_by(id = 1).one().characters:
            print character


    session.commit()

