# need to do cards
# cardname : cost : type : resource generated : special tag
# types: monster / construct / weapon / hero
# potential issue - having zero cards in deck via banishing - trying to draw a new card etc

from random import shuffle
import csv

# personal note:
# extend concatenates two lists
# append adds the item to the end
# hence the issue that was being caused by hands full of letters

# cardName: [runes generated, power generated, honour, cost]
# this will be populated from the csv file
card_list = {"Apprentice":[1, 0, 0, 0], "Militia":[0,1,0,0]}

# need a print value for cards to make information clearer [Apprentice // 1 Rune // 0 Honour] [ MONSTER: Name // x Power // y Honour // z Special Effects]

def handInstructions():
	"""tells the player what to do"""
	print "To play a card, input the number next to the card."
	print "Enter 'END' to end your turn"

class deck(object):
	"""This is a base used for player decks and the game 'deck'"""
	# game hand = board, discard = banish (used by players also), power = remaining resources etc.
	def __init__(self, name):
		self.name = name
		self.deck = []
		self.hand = []
		self.discard = []


class player(deck):
	"""each individual player"""
	def __init__(self, name):
		super(player, self).__init__(name)
		self.honour = 0
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

	def drawCard(self):
		# do i need to account for the incredibly unlikely event of discard and deck having no cards in them?
		if len(self.deck) == 0:
			self.deck = list(self.discard)
			self.discard = []
			shuffle(self.deck)
		self.discard.append(self.deck[0])
		self.hand.append(self.deck.pop()) # assume this pops the 0'th indexed item by default but havet to check

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
					addRunes = card_list[self.hand[cardIndex]][0] 
					addPower = card_list[self.hand[cardIndex]][1]
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

#>>>>>>>>>>>>>>>>>>>>>>>>>>>

x = player("Steve")

print x.deck
#x.newDeck()
#x.newHand()
x.playHand()

"""class board(object):
	def __init__(self):
		self.deck = []
		self.constants = {}
		self.board = {}


class monsterDeck(object):
	""Monster / Central deck"
	def __init__(self):
		self.deck = []
		self.discard = []


with open('CotG.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row[1]

# probably best to front load this information into memory when first run
"""