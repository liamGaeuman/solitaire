import random
class Card:
    rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    suit = ["Spades", "Hearts", "Clubs", "Diamonds"]
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def image(self):
        if (self.suit == "Spades"):
            return str(self.rank) + "s" + ".gif"
        elif (self.suit == "Hearts"):
            return str(self.rank) + "h" + ".gif"
        elif (self.suit == "Clubs"):
            return str(self.rank) + "c" + ".gif"
        else:
            return str(self.rank) + "d" + ".gif"

    def __str__(self):
        if (self.rank == 1):
            return "Ace of " + self.suit
        elif (self.rank == 11):
            return "Jack of " + self.suit
        elif (self.rank == 12):
            return "Queen of " + self.suit
        elif (self.rank == 13):
            return "King of " + self.suit
        else:
            return str(self.rank) + " of " + self.suit
            
##     OverLoad comparison operators 
##    def __lt__(self, other):
##        if(self.a<other.a):
##            return "ob1 is less than ob2"
##        else:
##            return "ob2 is less than ob1"
##    def __eq__(self, other):
##        if(self.a == other.a):
##            return "Both are equal"
##        else:
##            return "Not equal"

class Deck():
    """ A deck containing 52 cards."""
    
    def __init__(self):
        """Creates a full deck of cards.""" #make this inherit from list?
        self.deck = []

        for suit in Card.suit:        
            for rank in Card.rank:
                card = Card(rank, suit)
                self.deck.append(card)

    def shuffle(self):
        """Shuffles the cards."""
        random.shuffle(self.deck)

    def deal(self):
        """Removes and returns the top card or None 
        if the deck is empty."""
        if len(self) == 0:
           return None
        else:
            return self.deck.pop()

    def __len__(self):
       """Returns the number of cards left in the deck."""
       return len(self.deck)

    def __str__(self):
        """Returns the string representation of a deck."""
        deckString = ""
        for card in self.deck:
             deckString += str(card) + "\n"
        return deckString
    



