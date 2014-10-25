from pyscension import *

#>>>>>>>>>>>>>>>>>>>>>>>>>>>

x = player("Steve")
y = player("McManaman")

players = [x, y]

gameBoard = board("GAME BOARD") # here for testing but should probably move name to be a player specific attribute
# z.displayBoard()
# playHand(x, gameBoard)

'''def playGame(players, gameBoard):
	z = ""
	while z.upper() != "END GAME":
		for player in players:
			z = raw_input("type 'END GAME' to end the game, anything else to continue: ")
			if z.upper() == 'END GAME':
				break
			playHand(player, gameBoard)

playGame(players, gameBoard)
'''
playGame()

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