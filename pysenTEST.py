from pyscension import *

#>>>>>>>>>>>>>>>>>>>>>>>>>>>

x = player("Steve")
z = board("GAME BOARD") # here for testing but should probably move name to be a player specific attribute
z.displayBoard()
playHand(x, z)
#print x.deck
#x.newDeck()
#x.newHand()
#x.playHand()
#print displayCard("Apprentice")
#print displayCard("Heavy Infantry")
#print displayCard(z.hand[0])
#print board_cards
#print 'Wind Tyrant' in board_cards
#print displayCard('Wind Tyrant')
#print displayCard('Wind Tyrant', True)

# testing the new gameCard class
# print displayCard("Mistake of Creation")