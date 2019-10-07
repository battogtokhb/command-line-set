# Command Line Set

![game screenshot](game-screenshot.png)

## Overview
A fun command line implementation of the popular card game Set. 

## Instructions 

1. Download/clone this repository
2. Set up and activate a `virtualenv`
3. Run `pip install -r requirements.text` 
4. Run `./main`
5. For best results, please do not resize the terminal window

## Rules 
The objective of this single player game is to identify a set of three cards. Each card has four features: shape, color, number, and shading which each can vary in 3 ways. Therefore, there are 81 cards in the game total. For each one of the 4 features, 3 cards (a set) must display that feature as either all the same, or all different. If two cards are the same and 1 card is different in any feature, then it is not a set. 

The user is presented with 12 cards initally, and obtains three points for every set found. The user may obtain hints at the cost of one point. And the user may also draw more cards if a set cannot be found in the displayed cards (a point will be deducted if a user attempts to draw more cards when there is at least one existing set). 


Please refer to [Wikipedia](https://en.wikipedia.org/wiki/Set) for more detailed instructions.

## Design Choices
Each feature is represented with an enumeration because enums provide immutability and semantic meaning. A card is a class, and we take advantage of the ability to set custom string representations for a class object to display each card in the terminal. A game of set is a class as well and includes functions like displaying the cards to the terminal and drawing cards from the deck. This allows us to easily represent a game in `main.py`.

Whenever we change the cards displayed to the user