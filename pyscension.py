# need to do cards
# cardname : cost : type : resource generated : special tag
# types: monster / construct / weapon / hero
# potential issue - having zero cards in deck via banishing - trying to draw a new card etc

from random import shuffle

# personal note:
# extend concatenates two lists
# append adds the item to the end
# hence the issue that was being caused by hands full of letters

# cardName: [runes generated, power generated, honour, cost]
card_list = {"Apprentice":[1, 0, 0, 0], "Militia":[0,1,0,0]}


class player(object):
	def __init__(self, name):
		self.name = name
		self.deck = []
		self.newDeck()
		self.discard = []
		self.hand = []
		self.newHand()

		"""print self.name
		print "----"
		for card in self.deck:
			print card
		print "hand:", self.hand"""

		self.displayHand()


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
		# do i need to account for the incredibly unlikely event of a discard and deck having no cards in them
		if len(self.deck) == 0:
			self.deck = list(self.discard)
			self.discard = []
			shuffle(self.deck)
		self.discard.append(self.deck[0])
		self.hand.append(self.deck.pop()) # assume this pops the 0'th indexed item by default but havet to check

	def newHand(self):
		if len(self.hand) != 0:
			for card in self.hand:
				self.discard.append(card)
				self.hand = [] # would be cleaner using pop but for lists that requires iterating over the indexes
		for i in range(5):
			self.drawCard()
		
	def displayHand(self):
		print "%s hand:\n %s" % (self.name, [(i, card) for i in range(5) for card in self.hand]) # this does not provide the output I desire

x = player("Steve")

# these two need to be connected as a player has a single deck and a single hand - player class?
# scary new realms that may well require actual software enginerring prowess



