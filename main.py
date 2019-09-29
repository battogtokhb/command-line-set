import sys
import time
from game import SetGame


def intro():
    print ("Welcome to the card game Set. \n")
    print ("Each card shown has an identification number beneath the card. \n\n")

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
    while (numSetsShowing < 0):
        game = SetGame()
        game.showCards()
    game.showGameStatus()
    while (game.numCardsRemaining() > 0 and numSetsShowing > 0 and quit == False):
        validInput = False
        IDs = []
        while (validInput is False):
            userInput = input("Enter the ID numbers (space delimited) of three cards that form a set: ")
            if userInput == "quit" or userInput == "q":
                quit = True
                break
            splitWords = userInput.split()
            if (len(splitWords) == 3):
                for word in splitWords:
                    val = representsInt(word)
                    if (val is not None and val >= 0 and val < len(game.showingCards)) :
                        IDs.append(val)
            else:
                game.delete_last_line()
                print ("Invalid input. Please try again ...")
                time.sleep(1.5)
                game.delete_last_line()
                continue

            if len(IDs) == 3:
                break
            else:
                game.delete_last_line()
                print ("Invalid input. Enter three IDs. Please try again ...")
                time.sleep(1.5)
                game.delete_last_line()
                continue

        if (quit):
            print ("Thank you for playing. ")
            break

        isSet = game.validateSet(IDs)
        if (isSet):
            game.delete_last_line()
            print ("Congratulations! That was a set! ")
            time.sleep(1.5)
            game.delete_last_line()
            for index in IDs:
                game.replaceCardAt(index)
            numSetsShowing = game.findSets()
            game.showCards()
            game.showGameStatus()
            continue
        else:
            game.delete_last_line()
            print ("That was not a set! Please try again ...")
            time.sleep(1.5)
            game.delete_last_line()
            continue


if (__name__ == '__main__'):
    main()
