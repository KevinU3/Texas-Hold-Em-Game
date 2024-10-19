
## Module allows the user to play a game of Texas Hold 'em Poker
#


from Game import game
from Deck import cardDeck
import pygame

#sets up a game of poker
class poker(game):
    ## Initializes required instance variables for the object
    # @param width an integer that represents the width length of the canvas
    # @param height an interger that represents the height length of the canvas
    # @param pot an integer that represents the initial pot value
    # @param playerStartingMoney an integer representing player's initial money
    def __init__(self, width, height, pot = 0, playerStartingMoney = 0):
        super().__init__(width, height)
        self._width = width
        self._originalWidth = width
        self._height = height
        self._widthMiddleCards = width #to record the position of the cards in the middle to continue drawing cards relative to its position in the middle of the game
        self._middleCardsTotal = 3 #record the total cards in the middle of the canvas at the start of the game
        self._potValue = pot
        self._playerBankAmount = round(abs(playerStartingMoney),2) #ensure player's money is properly displayed
        super().addPlayerBankAmount("$"+str(self._playerBankAmount), 40, width / 6 - 100, height / 2 + 250)
        self._deck = set() #to create and record changes in the deck for the poker game
        self._aICards = set()
        self._playerCards = set()
        self.drawCard(self._widthMiddleCards, self._height, 3) #draw cards at the middle of the canvas
        self.drawCard(self._width, self._height, 2, player = True) #draw cards for the player
        self.drawCard(self._width, self._height,2, aI = True) #draw cards for the AI
        self.controlKey() #allow players to check, raise, or fold


    ## Draws cards onto the canvas
    # @param width an integer that represents the width length of the canvas
    # @param height an interger that represents the height length of the canvas
    # @param cards an integer representing the number of cards to be drawn
    # @param player a boolean representing cards drawn for the player; default is False
    # @param aI a boolean representing cards drawn for the computer; default is False
    def drawCard(self, width, height, cards, player = False, aI = False, fold = False):
        #place cards at the center
        xAxis = (width/2) - 50 #recenter the cards
        height = height/2
        if player == True:
            height = (height/2) + 500 #changes the card position to the player's area
            while cards > 0:
                card = cardDeck(xAxis, height, deck = tuple(self._deck)) #initializes all necessary initial variables of a card deck; convert to tuple to prevent hashing error
                cardChanges = card.changesInDeck() #obtain the card type that was drawn from the deck
                for i in range(len(cardChanges)):
                    self._deck.add(cardChanges[i]) #record the card that was drawn to prevent drawing duplicates from the deck
                    self._playerCards.add(cardChanges[i]) #record the cards in player's hand
                super().addSprite(card)
                xAxis = xAxis + 15 #move the next card to the right when a card is added to the canvas
                cards = cards - 1
        elif player == False and aI == True:
            height = (height/2) - 40 #changes the card position to the computer's area
            while cards > 0:
                if fold == True: #activates when player folds or when middle card reaches 5 cards
                    aI = False
                    card = cardDeck(xAxis, height, aI, deck = tuple(self._deck))
                    cardChanges = card.changesInDeck()
                    for i in range(len(cardChanges)):
                        self._deck.add(cardChanges[i])
                        self._aICards.add(cardChanges[i]) #record the cards AI has at hand
                    super().addSprite(card)
                else: #when player did not fold or game has not ended
                    card = cardDeck(xAxis, height, aI, deck = tuple(self._deck))
                    cardChanges = card.changesInDeck()
                    super().addSprite(card)
                xAxis = xAxis + 15 #move the next card to the right when a card is added to the canvas
                cards = cards - 1
        while cards > 0: #sets up the main card set on canvas
            card = cardDeck(xAxis, height, deck = tuple(self._deck))
            cardChanges = card.changesInDeck()
            for i in range(len(cardChanges)):
                self._deck.add(cardChanges[i])
                self._aICards.add(cardChanges[i]) #record cards in the center of the canvas
                self._playerCards.add(cardChanges[i])
            super().addSprite(card)
            xAxis = xAxis + 15  # move the next card to the right when a card is added to the canvas at the start of the game
            self._widthMiddleCards = self._widthMiddleCards + 30 #move position of middle cards when drawn in the middle of the game
            cards = cards - 1

    ## Start the match by drawing cards to players
    def resetMatch(self):
        self._middleCardsTotal = 3
        self._width=self._originalWidth
        self._widthMiddleCards=self._originalWidth
        self._deck = set() #to create and record changes in the deck for the poker game
        self._aICards = set()
        self._playerCards = set()
        super().__init__(self._width, self._height)
        super().addPlayerBankAmount("$" + str(self._playerBankAmount), 40, self._width / 6 - 100, self._height / 2 + 250)
        self.drawCard(self._widthMiddleCards, self._height, 3) #draw cards at the middle of the canvas
        self.drawCard(self._width, self._height, 2, player = True) #draw cards for the player
        self.drawCard(self._width, self._height,2, aI = True) #draw cards for the AI
        super().resetMatch()

    ## Allow players to control the sprite with keyboard
    def controlKey(self):
        super().controlKey()
        keys = pygame.key.get_pressed()
        if(self._gameDone==True): 
            if(keys[pygame.K_4]):
                self.resetMatch()
            return
        gameFinish = False
        foldStatus = False

        if keys[pygame.K_1]: #check
            self._middleCardsTotal = self._middleCardsTotal + 1 #record the increase in middle cards when a new card is drawn to the middle of the canvas
            if self._middleCardsTotal == 5: #when 5 cards are drawn to the middle of the canvas
                foldStatus = True #activates drawCard() to draw two cards for the AI to reveal to the player
                self.drawCard(self._widthMiddleCards, self._height, 1) #draw one card to the middle of the canvas
                self.drawCard(self._width, self._height, 2, aI = True,fold = foldStatus) #draws two card for AI to reveal
            else:
                self.drawCard(self._widthMiddleCards, self._height, 1)

        if keys[pygame.K_2]: #raise
            if self._playerBankAmount >= game.minimumWage: #does not activate when player does not have enough money to bet
                self._potValue = self._potValue + game.minimumWage + game.minimumWage #AI matches the raise of the player
                super().addText('$' + str(self._potValue), 60, self._width / 6 - 20, (self._height / 2) - 100) #change pot value shown to player
                self._playerBankAmount = self._playerBankAmount - game.minimumWage
                self._playerBankAmount = round(self._playerBankAmount,2) #round floats to two decimal points
            super().addPlayerBankAmount("$" + str(self._playerBankAmount), 40, self._width / 6 - 100, self._height / 2 + 250)

        if keys[pygame.K_3]: #fold
            foldStatus = True
            self.drawCard(self._width, self._height, 2, aI = True, fold = foldStatus)
            gameFinish = True

        if self._middleCardsTotal == 5 and self._middleCardsTotal != 3 and self._middleCardsTotal !=4 and foldStatus == True or gameFinish == True: #activates when game is done
            winner = self.checkHand(self._playerCards, self._aICards)
            super().addText('$' + str(self._potValue), 60, self._width / 6 - 20, (self._height / 2) - 100) #change pot value shown to player
            super().addPlayerBankAmount("$" + str(self._playerBankAmount), 40, self._width / 6 - 100, self._height / 2 + 250)
            self._playerBankAmount = round(self._playerBankAmount,2) #round floats to two decimal points
            super().addWinner(winner[0], 60, (self._width / 2) -100, (self._height / 2) + 40)
            super().addWinnerHand(winner[1], 60, (self._width / 2) +120, (self._height / 2)-70)
            super().gameDone() #to allow outcome of game to be displayed on screen

    ## Split the pot to ai and player
    def splitPot(self):
        gain = self._potValue/2
        self.resetPot()
        self._playerBankAmount += round(abs(gain),2)
    
    ## Set pot value to 0
    def resetPot(self):
        self._potValue =0

    ## Player gets the whole pot
    def gainFullPot(self):
        self._playerBankAmount+=round(abs(self._potValue),2)
        self.resetPot();

    ## Determines the winner of the Texas hold'em poker
    # @param player a tuple representing all the cards of the player
    # @param aI a tuple representing all the card of the aI
    # @return a tuple of result
    def checkHand(self, player, aI):
        #check for royal flush
        royalFlushPlayer = self.royalFlush(player)
        royalFlushAI = self.royalFlush(aI)
        if royalFlushPlayer == True and royalFlushAI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Royal Flush")
        elif royalFlushPlayer == True:
            self.gainFullPot()
            return ("Player wins", "Royal Flush")
        elif royalFlushAI == True:
            self.resetPot()
            return ("Computer wins", "Royal Flush")

        #check for straight Flush
        straightFlushPlayer = self.straightFlush(player)
        straightFlushaI = self.straightFlush(aI)
        if straightFlushPlayer == True and straightFlushaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Straight Flush")
        elif straightFlushPlayer == True:
            self.gainFullPot()
            return ("Player wins","Straight Flush")
        elif straightFlushaI == True:
            self.resetPot()
            return ("Computer wins", "Straight Flush")

        #check for four of a kind
        fourOfaKindPlayer = self.fourOfAkind(player)
        fourOfaKindaI = self.fourOfAkind(aI)
        if fourOfaKindPlayer == True and fourOfaKindaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Four Of A Kind")
        elif fourOfaKindPlayer == True:
            self.gainFullPot()
            return ("Player wins", "Four Of A Kind")
        elif fourOfaKindaI == True:
            self.resetPot()
            return ("Computer wins", "Four Of A Kind")

        #check for full house
        fullHousePlayer = self.fullHouse(player)
        fullHouseaI = self.fullHouse(aI)
        if fullHousePlayer == True and fullHouseaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Full House")
        elif fullHousePlayer == True:
            self.gainFullPot()
            return ("Player wins", "Full House")
        elif fullHouseaI == True:
            self.resetPot()
            return ("Computer wins", "Full House")

        #check for flush
        flushPlayer = self.flush(player)
        flushaI = self.flush(aI)
        if flushPlayer == True and flushaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Flush")
        elif flushPlayer == True:
            self.gainFullPot()
            return ("Player wins", "Flush")
        elif flushaI == True:
            self.resetPot()
            return ("Computer wins", "Flush")

        #check for straight
        straightPlayer = self.straight(player)
        straightaI = self.straight(aI)
        if straightPlayer == True and straightaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Straight")
        elif straightPlayer == True:
            self.gainFullPot()
            return ("Player wins", "Straight")
        elif straightaI == True:
            self.resetPot()
            return ("Computer wins", "Straight")

        #check for three of a kind
        threeOfaKindPlayer = self.threeOfaKind(player)
        threeOfaKindaI = self.threeOfaKind(aI)
        if threeOfaKindPlayer == True and threeOfaKindaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Three Of a Kind")
        elif threeOfaKindPlayer == True:
            self.gainFullPot()
            return ("Player wins", "Three Of a Kind")
        elif threeOfaKindaI == True:
            self.resetPot()
            return ("Computer wins", "Three Of a Kind")

        #check for two pairs
        twoPairsPlayer = self.twoPairs(player)
        twoPairsaI = self.twoPairs(aI)
        if twoPairsPlayer == True and twoPairsaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Two Pairs")
        elif twoPairsPlayer == True:
            self.gainFullPot()
            return ("Player wins", "Two Pairs")
        elif twoPairsaI == True:
            self.resetPot()
            return ("Computer wins", "Two Pairs")

        #check for pair
        pairPlayer = self.pair(player)
        pairaI = self.pair(aI)
        if pairPlayer == True and pairaI == True:
            self.splitPot();
            return ("Tie, Pot split.", "Pairs")
        elif pairPlayer == True:
            self.gainFullPot()
            return ("Player wins", "Pairs")
        elif pairaI == True:
            self.resetPot()
            return ("Computer wins", "Pairs")

        #check for high card winner
        playerWins = self.highCard(player, aI)

        if playerWins:
            self.gainFullPot()
            return ("Player wins", "High Card")
        else:
            self.resetPot()
            return ("Computer wins", "High Card")

    ## Determines if hand is royal flush
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def royalFlush(self, cards):
        cards = set(cards)
        royalFlushC = set()
        royalFlushD = set()
        royalFlushH = set()
        royalFlushS = set()
        for i in "cdhs": #to gather all possible types of cards with the same number
            if i == 'c': #to group the cards by their type to later on compare
                royalFlushC.add(str(10) + str(i) +".gif")
                royalFlushC.add(str(11) + str(i) +".gif")
                royalFlushC.add(str(12) + str(i) +".gif")
                royalFlushC.add(str(13) + str(i) +".gif")
                royalFlushC.add(str(1) + str(i) +".gif")
            elif i == 'd':
                royalFlushD.add(str(10) + str(i) +".gif")
                royalFlushD.add(str(11) + str(i) +".gif")
                royalFlushD.add(str(12) + str(i) +".gif")
                royalFlushD.add(str(13) + str(i) +".gif")
                royalFlushD.add(str(1) + str(i) +".gif")
            elif i == 'h':
                royalFlushH.add(str(10) + str(i) +".gif")
                royalFlushH.add(str(11) + str(i) +".gif")
                royalFlushH.add(str(12) + str(i) +".gif")
                royalFlushH.add(str(13) + str(i) +".gif")
                royalFlushH.add(str(1) + str(i) +".gif")
            elif i == 's':
                royalFlushS.add(str(10) + str(i) +".gif")
                royalFlushS.add(str(11) + str(i) +".gif")
                royalFlushS.add(str(12) + str(i) +".gif")
                royalFlushS.add(str(13) + str(i) +".gif")
                royalFlushS.add(str(1) + str(i) +".gif")
        if cards==royalFlushC or cards==royalFlushD or cards==royalFlushH or cards==royalFlushS:
            return True
        else:
            return False

    ## Determines if hand is straight flush
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def straightFlush(self, cards):
        cards = set(cards)
        straightFlushC = set()
        straightFlushD = set()
        straightFlushH = set()
        straightFlushS = set()
        for i in "cdhs": #to gather all possible types of cards with the same number
            for j in range(1,14):
                if i == 'c':  # to group the cards by their type to later on compare
                    straightFlushC.add(str(j) + str(i) + ".gif")
                elif i == 'd':
                    straightFlushD.add(str(j) + str(i) + ".gif")
                elif i == 'h':
                    straightFlushH.add(str(j) + str(i) + ".gif")
                elif i == 's':
                    straightFlushS.add(str(j) + str(i) + ".gif")
        straightC = self.straight(straightFlushC)
        straightD = self.straight(straightFlushD)
        straightH = self.straight(straightFlushH)
        straightS = self.straight(straightFlushS)
        if (cards.issubset(straightFlushC) and straightC) or (cards.issubset(straightFlushD) and straightD) or (cards.issubset(straightFlushH) and straightH) or (cards.issubset(straightFlushS) and straightS):
            return True
        else:
            return False

    ## Determines if hand is four of a kind
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def fourOfAkind(self, cards):
        cards = set(cards)
        fourOfAkind={'1': set(), '2': set(), '3': set(), '4': set(), '5': set(), '6': set(), '7': set(), '8': set(), '9': set(), '10': set(),
                    '11': set(), '12': set(), '13': set()}
        
        # parse through key of fourOfAkind and add each card to its respective key value in dictionary
        for key in fourOfAkind:
            for card in cards:
                if((key in card) and (len(card)-5==len(key))): # take into account differentiating 1 and 11 by subtracting 5 which represents "c.gif" from card string thus comparing the number length
                    fourOfAkind[key].add(card)

        # evaluate for four of a kind
        for key in fourOfAkind:
            if(fourOfAkind[key]==None):
                continue
            if(len(fourOfAkind[key])==4):
                return True
        return False #returns false after the cards set fail to match the four of a kind set

    ## Determines if hand is full house
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def fullHouse(self, cards):
        cards = list(cards)
        threeType = False
        twoType = False
        # get card count of hand
        fullHouse = self.countCards(cards)
        #ensure there are 3 of the same number and different types and two of another number and different types
        for key in fullHouse:
            if fullHouse[key]>=3:
                threeType = True
                continue
            if fullHouse[key]>=2:
                twoType = True
                continue
        if threeType == True and twoType == True:
            return True
        else:
            return False

    ## Determines if hand is flush
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def flush(self, cards):
        cards = set(cards)
        types = {'c':0, 'd':0, 'h':0, 's': 0}
        isFlush = False
        #count the card types
        for card in cards:
            if('c' in card):
                types['c']=types['c']+1
            if('d' in card):
                types['d']=types['d']+1
            if('h' in card):
                types['h']=types['h']+1
            if('s' in card):
                types['s']=types['s']+1

        #find if there are 5 cards of the same type
        for key in types:
            if types[key]>=5:
                isFlush=True

        return isFlush

    ## Determines if hand is straight
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def straight(self, cards):
        cards = list(cards)
        card = []
        numbers = []
        hand= set()
        isFullHand = False
        isStraight = True
        diff=0
        #simplify string
        for i in cards:
            i = i.split(".")
            card.append(i[0])
        #extract numbers
        for i in card:
            if len(i) == 3:
                numbers.append(int(i[0:2])) #extract number and turn to integer
            elif len(i) == 2:
                numbers.append(int(i[0]))
        numbers.sort() #sort ascending order

        #determine if the cards are a straight hand
        for i in range(len(numbers)):
            if len(hand) == 5: #player has a full hand of possible straight
                isFullHand = True
                break
            if(len(numbers)-1!=i):
                diff = abs(numbers[i] - numbers[i+1])
                if(diff == 1):
                    hand.add(numbers[i])
                    hand.add(numbers[i+1])

        hand = list(hand)

        #if player hand is empty then there is no possibility of straight
        if(len(hand)==0):
            return False
        
        #get first value to test for straight
        testValue= hand.pop(0)
        for card in hand:   
            testValue = testValue +1
            #if the cards do not match then we don't have a straight
            if(testValue != card):
                isStraight=False
                break
        #if player has a full hand of 5 cards and the cards are straight then return true
        if isStraight and isFullHand:
            return True
        else:
            return False

    ## Determines if hand is royal three of a kind
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def threeOfaKind(self, cards):
        cards = list(cards)
        isThreeOfaKind = False
        # count cards on hand
        threeOfaKind = self.countCards(cards)

        #ensure there are 3 of the same number and different types
        for key in threeOfaKind:
            if threeOfaKind[key]>=3:
                isThreeOfaKind = True
                break

        return isThreeOfaKind

    ## Determines if hand is two pairs
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def twoPairs(self, cards):
        return self.pair(cards, 2)

    ## Determines if hand is pair
    # @param cards a tuple representing the hand of cards
    # @return a boolean
    def pair(self, cards, requiredPair = 1):
        cards = list(cards)
        pairResult = False
        pairCount = 0

        #ensure there are 3 of the same number and different types
        pair = self.countCards(cards)
        for key in pair:
            if pair[key]>=2:
                pairCount = pairCount +1
            if pairCount == requiredPair:
                pairResult = True
                break
        return pairResult

    ## Determines if hand is high card
    # @param player a tuple representing the player hand of cards
    # @param aI a tuple representing the aI hand of cards
    # @return an boolean presenting the the winner of a highCard hand
    def highCard(self, player, aI):
        #extract numbers value from cards and remove duplicates
        playerCardsList = list(set(self.extractNumbers(player)))
        aICardsList = list(set(self.extractNumbers(aI)))

        #sort ascend for better comparision
        playerCardsList.sort()
        aICardsList.sort()

        #if player and ai has aces then remove them from both hands
        if(1 in playerCardsList and 1 in aICardsList):
            playerCardsList.pop(0)
            aICardsList.pop(0)
        #player has the biggest card an ace and wins
        elif(1 in playerCardsList):
            return True
        #ai has the biggest card an ace and wins
        elif(1 in aICardsList):
            return False
        
        #find the next largest card to compare from both player and ai
        totalCards = len(playerCardsList)
        while(totalCards):
            playerLargestCard = playerCardsList.pop()
            aILargestCard = aICardsList.pop()
            #if cards are not the same break loop, a match maker found
            if(playerLargestCard != aILargestCard):
                break
            totalCards=totalCards-1

        #if player card is larger then player wins
        return playerLargestCard>aILargestCard

    ## Find the largest card in a hand
    # @param cards a tuple representing the hand of cards
    # @return a string representation of the card value
    def largestCard(self, cards):
        cards = list(cards)
        highest=0

        #extract numbers
        numbers = self.extractNumbers(cards)

        numbers.sort(reverse = True) #sort descending order

        if(len(numbers) != 0 and numbers[-1]==1):
            return "1"

        if(len(numbers) != 0):
            highest = numbers.pop(0)

        # if highest == 1:
        #     return "Ace"
        # else:
        return str(highest)
    
    ## Clean up and convert a hand of cards into its integer value form for comparision
    # @param cards a tuple representing the hand of cards
    # @return a list of integers representing the hand of card values
    def extractNumbers(self, cards):
        card = []
        numbers = []
        #simplify string
        for i in cards:
            i = i.split(".")
            card.append(i[0])
        #extract numbers
        for i in card:
            if len(i) == 3:
                numbers.append(int(i[0:2])) #extract number and turn to integer
            elif len(i) == 2:
                numbers.append(int(i[0]))
        
        return numbers

    ## Count the quantity of every card in a hand
    # @param cards a tuple representing the hand of cards
    # @return a dictionary with key string representing the card value type and value integer representing the quantity of the card type in a hand
    def countCards(self, cards):
        dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0,
                    '11': 0, '12': 0, '13': 0}
        # fill in the dict dictionary to its respective number
        for key in dict:
            for card in cards:  # to go through all the different numbered cards
                card = self.largestCard(card)
                if key == card: #match card value to dict key
                    dict[key]= dict[key]+1
        
        return dict