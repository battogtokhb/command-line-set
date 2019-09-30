import sys
import time
from game import SetGame


def intro():
    print ("Welcome to the card game Set. Written by Zaya Battogtokh \n")
    print ("For a great experience, DO NOT resize your terminal window.")
    print ("Please read this Wikipedia page for gameplay: https://en.wikipedia.org/wiki/Set_(card_game)")
    print ("Cards have unique identification numbers.")
    print ("When promped, please enter the IDs (space delimited) of three cards that form a set.")
    print ("Enter 'hint' or 'draw [number]' at the prompt to either reveal a set or draw more cards.")
    print ("Enter 'q' or 'quit' at the prompt to quit the game. Enjoy! \n\n")

def representsInt(s):
    val = None
    try:
        if s[0] == '0' and s != "0":
            val = int(s[1:])
        else:
            val = int(s)
        return val
    except ValueError:
        return val

def main():
    intro()
    quit = False
    game = SetGame()
    game.showCards()
    numSetsShowing = game.findSets()

    def showBriefMessage(message):
        game.delete_last_line()
        print (message)
        time.sleep(1.5)
        game.delete_last_line()

    while (numSetsShowing < 0):
        game = SetGame()
        game.showCards()
    game.showGameStatus()
    while (game.numCardsRemaining() > 0 and numSetsShowing > 0 and quit == False):
        validInput = False
        IDs = []
        hintSet = game.getOneHintSet()
        while (validInput is False):
            userInput = input("Enter the ID numbers: ")
            if userInput == "quit" or userInput == "q":
                quit = True
                break

            if userInput.lower() == "hint":
                showBriefMessage(hintSet)
                continue

            splitWords = userInput.split()
            # if splitWords[0] == "draw":
            #     if len(splitWords) > 1:


            if (len(splitWords) == 3):
                for word in splitWords:
                    val = representsInt(word)
                    if (val is not None and val >= 0 and val < len(game.showingCards)) :
                        IDs.append(val)
            else:
                showBriefMessage("Invalid input. Please try again ...")
                continue

            if len(IDs) == 3:
                break
            else:
                showBriefMessage ("Invalid input. Enter three IDs. Please try again ...")
                continue

        if (quit):
            print ("Thank you for playing. ")
            break

        isSet = game.validateSet(IDs)
        if (isSet):
            showBriefMessage ("Congratulations! That was a set! ")
            for index in IDs:
                game.replaceCardAt(index)
            numSetsShowing = game.findSets()
            game.showCards()
            game.showGameStatus()
            continue
        else:
            showBriefMessage ("That was not a set! Please try again ...")
            continue

if (__name__ == '__main__'):
    main()
