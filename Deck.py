
## Module allows cards to be drawn randomly from a deck
#
from random import randint
import pygame

#draw card from deck for card game
class cardDeck(pygame.sprite.Sprite):

    ## Initializes required instance variables for the object
    # @param x an integer that represents the width length of the canvas
    # @param y an integer that represents the height length of the canvas
    # @param aI a boolean representing cards drawn for the computer; default is False
    # @param deck a tuple representing the deck of the game
    def __init__(self, x, y, aI = False, deck = tuple()):
        super().__init__()
        self._type = {0: 'c', 1: 'd', 2: 'h', 3: 's', 4: 'b'}
        self._deck = set()
        self._name = self.checkDeck(deck) #selects a card from the deck that has not been drawn
        self.loadCard(x, y, aI) #prepares to the card for pygame to draw onto the canvas

    ## Loads the card image into pygame sprite format
    # @param x an integer that represents the width length of the canvas
    # @param y an integer that represents the height length of the canvas
    # @param aI a boolean representing cards drawn for the computer
    def loadCard(self, x, y, aI):
        #draw card sprite
        if aI == False:
            sprite = pygame.image.load("./DECK/"+self._name) #retrieve image randonly
        else:
            sprite = pygame.image.load("./DECK/"+str(self._type[4]) + ".gif")  # retrieve back card image
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x     #sets the x coordinates of the image on the canvas
        self.rect.y = y - self.rect.height  #sets the y coordinates of the image relative to the height of the image

    ## Selects a card from the deck that has not been drawn
    # @param return returns a string representing the name of the card image
    # @param deck a tuple representing the deck of the game
    # @return returns the name of the image file
    def checkDeck(self, deck):
        deck = set(deck) #convert deck from tuple to set to ensure cards are not drawn more than once from the deck
        while True:
            cardName = str(randint(1, 13)) + str(self._type[randint(0, 3)]) + ".gif"
            if cardName not in self._deck:
                if cardName not in deck: #ensure cards drawn to the canvas are not drawn again from the game deck
                    self._deck.add(cardName)
                    return cardName
    ## Return the name and type of the card drawn from the deck
    # @return returns a tuple representing the card that was drawn from the deck
    def changesInDeck(self):
        return tuple(self._deck) #convert to tuple to prevent hashing error
