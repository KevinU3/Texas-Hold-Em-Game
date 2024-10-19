##This file is a driver file for poker module
#

from Poker import poker

if __name__ == "__main__":
    a=poker(1000,1000, playerStartingMoney = 1000.226)
    a.runGame()