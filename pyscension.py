# need to do cards
# cardname : cost : type : resource generated : special tag
# potential issue - having zero cards in deck via banishing - trying to draw a new card etc

from random import shuffle
import csv

# personal note:
#  > extend concatenates two lists
#  > append adds the item to the end

card_list = {}
board_cards = []
board_constants = []
boardSymbols = ['q','w','e','r','t','y']
boardConstants = ['i','o','p'] # this should be replaced by something better and renamed
badMethod = {'q':0, 'w':1, 'e':2, 'r':3, 't':4, 'y':5} # note the variable name

# this generation could be made clearer by first assigning the rows to variables ie name = row[0], x.append(name)
with open('CotG.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	if row[0] == 'board':
    		for i in range(int(row[8])): # take account of the quantities
    			board_cards.append(row[1])
    	elif row[0] == 'constant':
    		board_constants.append(row[1])
    	if row[0] != 'skip':
    		cardName = row[1]
    		card_list[cardName] = {'cost':row[2], 'runes':row[3], 'power':row[4], 'honor':row[5], 'faction':row[6], 'type':row[7]}

def handInstructions():
	"""tells the player what to do"""
	print "To play a card, input the key next to the card."
	print "Enter 'END' to end your turn"

def displayCard(cardName, location = 'hand'): # this should not be a boolean but rather a string parameter that assumes hand but can also take board or constants
	"""takes in card details and outputs a single
	line summary of it - NEEDS REFACTORING
	IF MONSTER - power and honor come last, cost needs to be somewhere for board"""

	if int(card_list[cardName]['runes']) > 0:
		runes = card_list[cardName]['runes'] + "R"
	else:
		runes = ""

	if int(card_list[cardName]['power']) > 0:
		power = " / " if len(runes) > 0 else "" + card_list[cardName]['power'] + "P"
	else:
		power = ""

	if int(card_list[cardName]['honor']) > 0:
		honor = " // " if not board else ""
		honor += card_list[cardName]['honor'] + "h" # will need adjusting when stats are added in
	else:
		honor = ""

	if location == 'board':
		cost = card_list[cardName]['cost']
		strType = card_list[cardName]['type'].upper() + " " * (9 - len(card_list[cardName]['type']))

		if card_list[cardName]['type'].upper() == 'MONSTER':
			cost += " POWER"
		else:
			cost += " R    "

		strReturn = "%s - %s [%s%s%s] %s " % (strType, cost, runes, power, honor, displayCard(cardName))
	elif location == 'hand':
		strReturn = "[%s: %s%s%s]" % (cardName, runes, power, honor)
	elif location == 'constants':
		for i in range(3):
			strReturn = strReturn = "[%s: %s%s%s]" % (cardName, runes, power, honor)
			# this is the same as hand for now but can tweak this
			# potentially incorporate the key symbols into this instead of the deck
			# displayBoard function?
	else:
		strReturn = "ERROR: failed to display card correctly"

	return strReturn

class deck(object):
	"""This is a base used for player decks and the game 'deck' """
	def __init__(plyr, name):
		plyr.name = name
		plyr.deck = []
		plyr.hand = []
		plyr.constants = []
		plyr.discard = []
		plyr.honor = 0

	def drawCard(plyr):
		# do i need to account for the incredibly unlikely event of discard and deck having no cards in them?
		if len(plyr.deck) == 0:
			plyr.deck = list(plyr.discard)
			plyr.discard = []
			shuffle(plyr.deck)
		plyr.hand.append(plyr.deck.pop()) # assume this pops the 0'th indexed item by default but have to check

class board(deck):
	"""board state
	game hand = board, discard = banish (used by players also), power = remaining resources etc."""
	def __init__(self, name):
		super(board, self).__init__(name)
		self.newDeck()
		self.newHand()	

	def newDeck(self): # these should be wrapped with a "new game" function
		self.deck = []
		self.constants = [] # should move this all to a separate function to reset it all, just call init again with the name?
		for key in board_cards:
			self.deck.append(key)
		shuffle(self.deck)
		for card in board_constants:
			self.constants.append(card)

	def newHand(self):
		for i in range(6):	# any value to a global variable for cards in hand?
			self.drawCard()

	def displayBoard(self):
		print "=" * 10
		print "Constants: \n %s // %s // %s" % (boardConstants[0] + ": " + displayCard("Cultist", "constants"), boardConstants[1] + ": " + displayCard("Mystic", "constants"), boardConstants[2] + ": " + displayCard("Heavy Infantry", "constants"))
		#print "Constants: \n [MONSTER: Cultist - 2P - 1h]  // [Mystic - 2R - 1h] // [Heavy Infantry - 2P - 1h]"
		print "Board:"
		for i in range(6):
			print "\t" + boardSymbols[i] + ": " + displayCard(self.hand[i], 'board')
			#print "\t", card_list[self.hand[i]][5].upper(), ":", self.hand[i]
		print "-" * 10

class player(deck):
	"""each individual player"""
	def __init__(self, name):
		super(player, self).__init__(name)
		self.newDeck() # should these be moved to their own method with the parent class now taking precedence?
		self.newHand()
		self.power = 0
		self.runes = 0

	def newDeck(self):
		"""player crafted deck - starts with:
		8 Apprentice
		2 Militia"""
		self.deck = []
		for i in range(8):
			self.deck.append("Apprentice")
		for i in range(2):
			self.deck.append("Militia")
		shuffle(self.deck)
		self.discard = []

	def newHand(self):
		#this could be simplified to discard hand // new hand to have a single unified parent method that just draws to five - would work for the game state and the player
		if len(self.hand) != 0:
			for card in self.hand:
				self.discard.append(card)
				self.hand = [] # would be cleaner using pop but for lists that requires iterating over the indexes - why does this mean I can't use pop?
		for i in range(5):	# any value to a global variable for cards in hand?
			self.drawCard()
		
	def displayHand(self):
		# print "%s hand:\n %s" % (self.name, [(i, card) for card in self.hand for i in range(5)]) # this does not provide the output I desire
		print "%s's hand:" % self.name
		for x in range(len(self.hand)):
			print x + 1,":", displayCard(self.hand[x], 'hand')
			# old method:
			# print x,":", self.hand[x] # intention is for hand to be interacted with via numbers whilst the board/game is via letters (iterate over a list ['q','w','e', etc])



def acquireCard(plyr, dck, cardName):
	"""buy cards"""
	# foo = 'defeated' if card_list[cardName]['type'].upper() == 'MONSTER' else 'purchased'
	if card_list[cardName]['type'].upper() == 'MONSTER':
		if plyr.power < card_list[cardName]['power']:
			print "+" * 10
			print "You do not have enough power to defeat %s." % cardName
		else:
			plyr.power -= card_list[cardName]['power']
			plyr.discard.append(cardName)
			dck.hand.remove(cardName)
			dck.drawCard()

			foo = 'defeated'
			print '~' * 10
			print "You %s %s" % (foo, cardName)
	else:
		if plyr.runes < card_list[cardName]['runes']:
			print "+" * 10
			print "You do not have enough runes to purchase %s." % cardName
		else:
			plyr.discard.append(cardName)
			dck.hand.remove(cardName)
			dck.drawCard()
			
			foo = 'purchased'
			print '~' * 10
			print "You %s %s" % (foo, cardName)
	

def playHand(plyr, dck):

		handInstructions()
		cardSel = ""
		plyr.runes = 0
		plyr.power = 0

		#while len(plyr.hand) != 0:
		while cardSel.upper() != 'END':
			print "~" * 10
			plyr.displayHand()
			print "runes: %s // power: %s" % (plyr.runes, plyr.power)

			cardSel = raw_input(":")

			if cardSel.upper() == "END":
				break

			if cardSel in boardSymbols:
				cardName = dck.hand[badMethod[cardSel]] # note the name of the method
				acquireCard(plyr, dck, cardName)
				dck.displayBoard()
				
			# these checks for valid input need sorting out, perhaps their own section
			# or maybe just have a binary split between is digit and otherwise that run the relevant check for the given input type
			elif cardSel.isdigit():
				cardIndex = int(cardSel)
				if cardIndex > len(plyr.hand) or cardIndex <= 0:
					print "~" * 10
					print "Invalid Entry. Try Again"
				else:
					cardIndex -= 1
					addRunes = int(card_list[plyr.hand[cardIndex]]['runes'])
					addPower = int(card_list[plyr.hand[cardIndex]]['power'])
					print "~" * 10
					print "Played %s gaining %s runes and %s power." % (plyr.hand[cardIndex], addRunes, addPower)
					plyr.discard.append(plyr.hand.pop(cardIndex))
					plyr.runes += addRunes 
					plyr.power += addPower
			else:
				print "~" * 10
				print "Invalid Entry. Try Again"

		print "---Ending Turn---"


# could simplify the game by rather than having to play cards simply calculates the current resources of the player
# guess it depends on what you see as part of the game - is the agility part of it or is it the decisions
# also card draw, constructs etc
