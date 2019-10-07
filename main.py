import sys
import time
from colorama import Fore
from colorama import Style
from game import SetGame


def intro():
    print ("Welcome to Set. Written by Zaya Battogtokh. \n")
    print ("The objective is to identify a set of three cards.")
    print ("Each card has four features: shape, color, number, and shading which each can vary in 3 ways:")
    print ("Shape: ⬥, ◼, ●  [diamond, square, circle]")
    print ("Color:" + Fore.RED + " ◼" + Style.RESET_ALL + "," + Fore.GREEN + " ◼" + Style.RESET_ALL + "," + Fore.MAGENTA + " ◼" + Style.RESET_ALL  + " [red, green, purple]")
    print ("Number: ⬥, ⬥ ⬥, ⬥ ⬥ ⬥ [one, two, three]")
    print ("Shading: ◼, ◨, □ [filled, half-filled, open]")
    print ("\nFor each one of the 4 features, 3 cards (a set) must display that feature as either all the same, or all different. \n")

    print ("Cards have unique identification numbers. When promped, enter the IDs (space delimited) of 3 cards that form a set.")
    print ("Enter 'hint' or 'draw' at the prompt to either reveal a set or draw 3 more cards.")
    print ("Enter 'q' or 'quit' at the prompt to quit the game. Enjoy! \n")

    print ("For a great experience, DO NOT resize your terminal window.\n\n")


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

    def showBriefMessage(message, length=1.5):
        game.delete_last_line()
        print (message)
        time.sleep(length)
        game.delete_last_line()

    while (numSetsShowing == 0):
        game = SetGame()
        numSetsShowing = game.findSets()
        game.showCards()

    game.showGameStatus()
    while (game.numCardsRemaining() > 0 and quit == False):
        validInput = False
        IDs = []
        while (validInput is False):
            hintSet = game.getOneHintSet()
            userInput = input("Enter the ID numbers: ")
            if userInput == "quit" or userInput == "q":
                quit = True
                break

            if userInput.lower() == "hint":
                game.updateScore(-1)
                message = ""
                if hintSet is None:
                    message = "No sets can be formed! Please draw more cards."
                else:
                    message = hintSet

                showBriefMessage(message)
                game.showGameStatus(update=True)
                continue

            if userInput.lower() == "draw":
                if (numSetsShowing > 0):
                    game.updateScore(-1)
                    showBriefMessage("Cannot draw more cards when a set exists among existing cards!", length=2.5)
                    continue

                if (len(game.deck) == 0):
                    quit = True
                    break

                game.drawCards(3)
                numSetsShowing = game.findSets()
                game.delete_last_line()
                game.showCards()
                game.showGameStatus()
                continue

            splitWords = userInput.split()

            if (len(splitWords) == 3):
                for word in splitWords:
                    val = representsInt(word)
                    if (val is not None and val >= 0 and val < len(game.showingCards)) :
                        IDs.append(val)
            else:
                showBriefMessage("Invalid input. Please try again...")
                continue

            if len(IDs) == 3:
                break
            else:
                showBriefMessage ("Invalid input. Enter three IDs. - %d , %s - Please try again..." % (len(IDs), IDs) )
                continue

        if (quit):
            print ("Thank you for playing. Your final score is: %d." % game.score )
            break

        isSet = game.validateSet(IDs)
        if (isSet):
            showBriefMessage ("Congratulations! That was a set! ")
            selectedCards = []
            for index in IDs:
                selectedCards.append(game.showingCards[index])

            for card in selectedCards:
                game.replaceCard(card)

            numSetsShowing = game.findSets()
            game.updateScore(3)
            game.showCards()
            game.showGameStatus()
            continue
        else:
            showBriefMessage ("That was not a set! Please try again ...")
            game.updateScore(-1)
            game.showGameStatus(update=True)
            continue



if (__name__ == '__main__'):
    main()
