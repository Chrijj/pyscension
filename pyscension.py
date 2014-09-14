# need to do cards
# cardname : cost : type : resource generated : special tag
# potential issue - having zero cards in deck via banishing - trying to draw a new card etc

from random import shuffle
import csv

# personal note:
# extend concatenates two lists
# append adds the item to the end
# hence the issue that was being caused by hands full of letters

# cardName: [runes generated, power generated, honour, cost]
# this will be populated from the csv file

"""
loading data from the csv file into program memory

name: [cost, runes, power, honor]
if it's a monster, the cost is the power required, else it is the runes to buy
"""

# should i just have a single card list to look up, still need to generate the decks though
card_list = {}
board_cards = []
board_constants = []

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
    		card_list[row[1]] = [row[2], row[3], row[4], row[5], row[6], row[7]] # [row[x] for x in range(1, 7)] ?

# at the moment it is: name: [ 0,cost, 1,runes, 2,power, 3,honor, 4,faction, 5,type] need a space for special details

# need a print value for cards to make information clearer [Apprentice // 1 Rune // 0 Honour] [ MONSTER: Name // x Power // y Honour // z Special Effects]
# also need to identify the board cards - monster / construct / hero
def displayCard(cardName, board = False):
	"""takes in card details and outputs a single
	line summary of it
	IF MONSTER - power and honor come last, cost needs to be somewhere for board"""
	#if card_list[cardName][-1].upper() == "MONSTER":
	# need displays for monsters on the board and heros / constracts showing the buy cost
	#if cardName in board_cards:
	if int(card_list[cardName][1]) > 0:
		runes = card_list[cardName][1] + "R"
	else:
		runes = ""

	if int(card_list[cardName][2]) > 0:
		power = " / " if len(runes) > 0 else "" + card_list[cardName][2] + "P"
	else:
		power = ""

	if int(card_list[cardName][3]) > 0:
		honor = " // " if not board else ""
		honor += card_list[cardName][3] + "h" # will need adjusting when stats are added in
	else:
		honor = ""

	if board:
		cost = card_list[cardName][0]
		strType = card_list[cardName][5].upper() + " " * (9 - len(card_list[cardName][5]))

		if card_list[cardName][5].upper() == 'MONSTER':
			cost += " POWER"
		else:
			cost += " R    "

		strReturn = "%s: %s [%s%s%s] %s " % (strType, cost, runes, power, honor, displayCard(cardName))
	else:
		strReturn = "[%s: %s%s%s]" % (cardName, runes, power, honor)

	return strReturn


def handInstructions():
	"""tells the player what to do"""
	print "To play a card, input the number next to the card."
	print "Enter 'END' to end your turn"

class deck(object):
	"""This is a base used for player decks and the game 'deck'"""
	def __init__(self, name):
		self.name = name
		self.deck = []
		self.hand = []
		self.constants = []
		self.discard = []
		self.honor = 0

	def drawCard(self):
		# do i need to account for the incredibly unlikely event of discard and deck having no cards in them?
		if len(self.deck) == 0:
			self.deck = list(self.discard)
			self.discard = []
			shuffle(self.deck)
		self.hand.append(self.deck.pop()) # assume this pops the 0'th indexed item by default but have to check

class board(deck):
	"""board state
	game hand = board, discard = banish (used by players also), power = remaining resources etc."""
	def __init__(self, name):
		super(board, self).__init__(name)
		self.newDeck()
		self.newHand()	

	def newDeck(self): # these should be called "new game"
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
		print "Constants: \n %s // %s // %s" % (displayCard("Cultist"), displayCard("Mystic"), displayCard("Heavy Infantry"))
		#print "Constants: \n [MONSTER: Cultist - 2P - 1h]  // [Mystic - 2R - 1h] // [Heavy Infantry - 2P - 1h]"
		print "Board:"
		for i in range(6):
			print "\t" + displayCard(self.hand[i], True)
			#print "\t", card_list[self.hand[i]][5].upper(), ":", self.hand[i]
		print "-" * 10

class player(deck):
	"""each individual player"""
	def __init__(self, name):
		super(player, self).__init__(name)
		self.newDeck() # should these be moved to their own method with the parent class now taking precedence?
		self.newHand()

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
			print x,":", self.hand[x] # intention is for hand to be interacted with via numbers whilst the board/game is via letters (iterate over a list ['q','w','e', etc])


	def playHand(self):
		# this will need simplifying so that it just forms part of a whole related to a game tuen
		# runes / power perhaps becoming part of the self that are then cleared at the end of the turn to facilitate this
		handInstructions()
		cardSel = ""
		runes = 0
		power = 0
		while len(self.hand) != 0:
			print "~" * 10
			self.displayHand()
			print "runes: %s // power: %s" % (runes, power)
			cardSel = raw_input(":")
			if cardSel.upper() == "END":
				break
			if not cardSel.isdigit():
				print "~" * 10
				print "You must enter a number:"
			else:
				cardIndex = int(cardSel)
				if cardIndex > len(self.hand) - 1 or cardIndex < 0:
					print "~" * 10
					print "Invalid Entry. Try Again"
				else:
					addRunes = int(card_list[self.hand[cardIndex]][1])
					addPower = int(card_list[self.hand[cardIndex]][2])
					print "~" * 10
					print "Played %s gaining %s runes and %s power." % (self.hand[cardIndex], addRunes, addPower)
					self.discard.append(self.hand.pop(cardIndex))
					runes += addRunes 
					power += addPower

		if len(self.hand) == 0:
			print "No cards left to play"
		print "---Ending Turn---"


# could simplify the game by rather than having to play cards simply calculates the current resources of the player
# guess it depends on what you see as part of the game - is the agility part of it or is it the decisions
# also card draw, constructs etc
