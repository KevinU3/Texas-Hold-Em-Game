## Module that allows a user to play a 2d gambling card game on their screen
#

import pygame


#sets up base of card game with bets
class game():
    minimumWage = 20 #sets minimum wages of bets to 20

    ## Initializes required instance variables for the object
    # @param width an integer that represents the width length of the canvas
    # @param height an interger that represents the height length of the canvas
    def __init__(self, width = 1000, height = 1000):
        pygame.init()
        self.width = width
        self.height = height
        self._display = pygame.display.set_mode((self.width, self.height))
        self._sprites = pygame.sprite.LayeredUpdates()
        self._gameDone = False

        #initialize to prevent errors from raising
        self._font = pygame.font.Font(None, 60)
        self._text= self._font.render("$0", True, pygame.Color('Blue'))
        self._positionText = (width/6 , (height/2) - 100)

        #initialize card game discriptions
        self._potFont = pygame.font.Font(None, 40) #setup the text font
        self._potText = self._potFont.render("POT", True, pygame.Color('Black')) #setup text color and text
        self._positionPot = (width/6, height/2-60) #setup text position

        self._wagesFont = pygame.font.Font(None, 40)
        self._wagesText = self._wagesFont.render("$"+ str(game.minimumWage) + "minimum wage", True, pygame.Color('Black'))
        self._positionWages = ((width/6)-100, (height/2)-10)

        self._fontBank = pygame.font.Font(None, 40)
        self._bankText= self._fontBank.render("Player's Bank", True, pygame.Color('Black'))
        self._positionTextBank = (width/6-100, height/2+300)

        self._fontPlayerMoney = pygame.font.Font(None, 40)
        self._playerMoneyText= self._fontPlayerMoney.render("", True, pygame.Color('Blue'))
        self._positionPlayerMoney = (width/6-100, height/2+250)

        self._fontInstruction = pygame.font.Font(None, 40)
        self._InstructionText= self._fontInstruction.render("Enter: 1 to Check, 2 to Raise, 3 to Fold, and 4 to Play Again", True, pygame.Color('Red'))
        self._positionInstruction = (width/6 -50, height/2+350)

        # self._log = pygame.font.Font(None, 40)
        # self._logText= self._log.render("Enter: 1 to Check, 2 to Raise, 3 to Fold, and 4 to Play Again", True, pygame.Color('Red'))
        # self._positionLog = (width/6 -50, height/2+350)

        self._fontWinner = pygame.font.Font(None, 0)
        self._winnerText= self._fontWinner.render("", True, pygame.Color('Blue'))
        self._positionTextWinner = (width, height)

    ## Add the sprite onto the game program canvas
    # @param sprite a string representing the file name or file path of the sprite image
    def addSprite(self, sprite):
        self._sprites.add(sprite)

    ## Add text onto the game program canvas
    # @param text a string representing the text to be written onto the canvas
    # @param font an integer presenting the font size of text
    # @param width an integer that represents the width length of the canvas
    # @param height an interger that represents the height length of the canvas
    def addText(self, text, font, width, height):
        self._font = pygame.font.Font(None, font)
        self._text= self._font.render(text, True, pygame.Color('Blue'))
        self._positionText = (width, height)

    ## Add winner text onto the game program canvas
    # @param text a string representing the text to be written onto the canvas
    # @param font an integer presenting the font size of text
    # @param width an integer that represents the width length of the canvas
    # @param height an interger that represents the height length of the canvas
    def addWinner(self, text, font, width, height):
        self._fontWinner = pygame.font.Font(None, font)
        self._winnerText= self._fontWinner.render(text, True, pygame.Color('Gold'))
        self._positionTextWinner = (width, height)

    ## Add winner hand text onto the game program canvas
    # @param text a string representing the text to be written onto the canvas
    # @param font an integer presenting the font size of text
    # @param width an integer that represents the width length of the canvas
    # @param height an interger that represents the height length of the canvas
    def addWinnerHand(self, text, font, width, height):
        self._fontWinnerHand = pygame.font.Font(None, font)
        self._winnerHandText= self._fontWinner.render(text, True, pygame.Color('Gold'))
        self._positionTextWinnerHand = (width, height)

    ## Add money to the player's bank
    # @param text a string representing the text to be written onto the canvas
    # @param font an integer presenting the font size of text
    # @param width an integer that represents the width length of the canvas
    # @param height an interger that represents the height length of the canvas
    def addPlayerBankAmount(self, amount, font, width, height):
        self._fontPlayerMoney = pygame.font.Font(None, font)
        self._playerMoneyText = self._fontPlayerMoney.render(str(amount), True, pygame.Color('Blue'))
        self._positionPlayerMoney = (width, height)

    ## Reset the game for another match
    # @return returns nothing
    def resetMatch(self):
        self._gameDone= False
    

    ## Activates game done when the game is finished
    # @return returns nothing
    def gameDone(self):
        self._gameDone=True

    ## Allow players to control the sprite with keyboard
    # @return returns nothing; a place holder
    def controlKey(self):
        return

    ## Runs the game
    def runGame(self):
        while True:
            for gameEvent in pygame.event.get():
                if gameEvent.type == pygame.QUIT:
                    pygame.quit() #Exits the game
                    exit(0) #to prevent raising errors when quiting the game
                elif gameEvent.type == pygame.KEYDOWN:
                    self.controlKey()
            self._sprites.update() #Refreshes the sprites to reflect changes due to player's action
            self._display.fill((0, 255, 0))
            self._sprites.draw(self._display) #Draws the sprites onto the canvas
            self._display.blit(self._text, self._positionText) #draws text to canvas
            self._display.blit(self._potText, self._positionPot)
            self._display.blit(self._wagesText, self._positionWages)
            self._display.blit(self._bankText, self._positionTextBank)
            self._display.blit(self._playerMoneyText, self._positionPlayerMoney)
            self._display.blit(self._InstructionText, self._positionInstruction)
            if self._gameDone == True:
                self._display.blit(self._winnerText, self._positionTextWinner)  # draws winner text to canvas
                self._display.blit(self._winnerHandText, self._positionTextWinnerHand)  # draws winner hand text to canvas
    
            pygame.display.update()

