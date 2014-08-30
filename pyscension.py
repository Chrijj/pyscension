# need to do cards
# cardname : cost : type : resource generated : special tag
# types: monster / construct / weapon / hero

from random import shuffle

# cardName: [runes generated, power generated, honour, cost]
generic_player_cards = {"Apprentice":[1, 0, 0, 0], "Militia":[0,1,0,0]}



class playerDeck(object):
	"""player crafted deck - starts with:
		8 Apprentice
		2 Militia"""
	def __init__(self, playerName):
		self.playerName = playerName
		self.deck = []
		for i in range(8):
			self.deck.append(generic_player_cards["Apprentice"])
		for i in range(2):
			self.deck.append(generic_player_cards["Militia"])

		for element in self.deck:
			print element 
			print


x = playerDeck("Test Deck")


