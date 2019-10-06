from enum import Enum
import math
import sys
import colorama
from colorama import Fore
from colorama import Style
from colorama import Back
import random

class Color(Enum):
    Red = 1
    Green = 2
    Purple = 3

    def visual(self):
        if self.name == "Red":
            return Fore.RED + Back.WHITE
        elif self.name == "Green":
            return Fore.GREEN + Back.WHITE
        else:
            return Fore.MAGENTA + Back.WHITE


class Shape(Enum):
    Diamond = 1
    Squiggle = 2
    Oval = 3

    def visual(self):
        if self.name == "Diamond":
             return ["⬥","⬗","⬦" ]
        elif self.name == "Squiggle":
            return ["◼", "◨", "□"]
        else:
            return ["●", "◑", "◯", ]

class Shading(Enum):
    Solid = 1
    Striped = 2
    Open = 3

class Number(Enum):
    One = 1
    Two = 2
    Three = 3
    def visual(self):
        if self.name == "One":
            return '    *    '
        elif self.name == "Two":
            return '   * *   '
        else:
            return ' *  *  * '

# Variations of shapes possible

class Card(object):
    def __init__(self, shape, shading, color, number):
        self.shape = shape
        self.shading = shading
        self.color = color
        self.number = number

    def __repr__(self):
        exactShape = self.shape.visual()[self.shading.value - 1]
        face = self.number.visual().replace("*", exactShape )
        return self.color.visual() + face + Style.RESET_ALL

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __eq__(self, other):
        return (self.shape == other.shape and self.shading == other.shading and self.color == other.color and self.number == other.number)

    def __hash__(self):
        return hash( (self.shape, self.shading, self.color, self.number) )

class SetGame(object):

    def __init__(self):
        colorama.init(autoreset=True)
        self.deck = []
        self.showingSets = set()
        self.showingCards = []
        #number of lines used to display game information (cards + deck), used to clear output appropriately
        self.numLines = 1
        for number in Number:
            for shading in Shading:
                for shape in Shape:
                    for color in Color:
                        self.deck.append(Card(shape, shading, color, number))

        random.shuffle(self.deck)
        self.drawCards(12)

    def numCardsRemaining(self):
        return len(self.showingCards) + len(self.deck)

    def findSets(self):

        visited = set()
        self.showingSets = set()

        for first in self.showingCards:
            for second in self.showingCards:
                if (first != second and (first, second) not in visited and (second, first) not in visited):
                    color = None
                    shape = None
                    number = None
                    shading = None
                    pair = (first, second)
                    if first.color == second.color:
                        color = first.color
                    else:
                        color = Color(6-first.color.value-second.color.value)

                    if first.shape == second.shape:
                        shape = first.shape
                    else:
                        shape = Shape(6-first.shape.value-second.shape.value)

                    if first.number == second.number:
                        number = first.number
                    else:
                        number = Number(6-first.number.value-second.number.value)

                    if first.shading == second.shading:
                        shading = first.shading
                    else:
                        shading = Shading(6-first.shading.value -second.shading.value)

                    third = Card(shape, shading, color, number)
                    if third in self.showingCards:
                        triple = tuple(sorted([first, second, third]))
                        self.showingSets.add(triple)
                    visited.add(pair)

        return len(self.showingSets)


    def drawCards(self, n):
        while (n > 0 and len(self.deck) > 0):
            self.showingCards.append(self.deck.pop())
            n -= 1

    def replaceCardAt(self, index):
        assert(index >= 0 and index < len(self.showingCards))
        newCard = self.deck.pop()
        self.showingCards[index] = newCard


    def showCards(self, hm=False):
        while (self.numLines):
            self.delete_last_line()
            self.numLines -= 1

        if (hm):
            return

        idealNumInRow = math.ceil(math.sqrt(len(self.showingCards) ) )
        i = 0
        numberOfShowingCards = len(self.showingCards)
        while (i < numberOfShowingCards):
            self.displayCards(i, min(i+idealNumInRow, numberOfShowingCards-1))
            i += idealNumInRow + 1



    # improve card status design later
    def showGameStatus(self):
        print ("⟪⟪⟪     ɢᴀᴍᴇ ꜱᴛᴀᴛᴜꜱ     ⟫⟫⟫")
        print (f'    ᴄᴀʀᴅꜱ ʀᴇᴍᴀɪɴɪɴɢ: {len(self.deck) + len(self.showingCards)}')
        print ('\n', end="")
        self.numLines += 3

    def validateSet(self, IDs):
        assert(len(IDs) == 3)
        cardOne, cardTwo, cardThree = self.showingCards[IDs[0]], self.showingCards[IDs[1]], self.showingCards[IDs[2]]
        trip = tuple(sorted([cardOne, cardTwo, cardThree]))
        if (trip in self.showingSets):
            return True

        return False

    def getOneHintSet(self):
        if (len(self.showingSets) <= 0):
            return None
        randomInt = random.randint(0, len(self.showingSets)-1 )
        ret = list(self.showingSets)[randomInt]
        return ret

    # function obtained from this stack overflow post:
    # https://stackoverflow.com/questions/19596750/is-there-a-way-to-clear-your-printed-text-in-python
    def delete_last_line(self):
        "Use this function to delete the last line in the STDOUT"
        # cursor up one line
        sys.stdout.write('\x1b[1A')
        # delete last line
        sys.stdout.write('\x1b[2K')

    def displayCards(self, start, end):
        number = end - start + 1
        if number > len(self.showingCards):
            return
        normal = Fore.BLACK + Back.WHITE + '         '
        label = ' [ #** ] '
        spacing = "  "
        for _ in range(2):
            for _ in range(number):
                print (normal , end = spacing)
            print ('\n', end = "")
            self.numLines += 1

        for i in range(start, end+1, 1):
            print (repr(self.showingCards[i]), end = spacing)
        print ('\n', end = "")
        self.numLines += 1

        for _ in range(2):
            for _ in range(number):
                print (normal , end = spacing)
            print ('\n', end = "")
            self.numLines += 1
        print ('\n', end = "")
        self.numLines += 1

        for i in range(start, end+1, 1):
            #need to pad single digits for proper alignment
            filled_label = label.replace("**", '%02d' % i)
            print (filled_label, end = spacing)
        print ('\n')
        self.numLines += 2
