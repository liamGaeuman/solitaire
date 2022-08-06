from cards import *

class SolitaireGame:
    
    def __init__(self):
        # Create a new deck of cards
        self._game_deck = Deck()
        
        # A matrix to hold downward facing cards in the bottom cards 
        self.down_deck_matrix = [] #[][]
        # A matrix to hold upward facing cards in the bottom cards 
        self.up_deck_matrix = [] #[][]
        # A list to hold all upward facing cards in the left hand corner
        self.up_left_corner_deck = []
        # A list to hold all downward facing cards in the left hand corner
        self.down_left_corner_deck = []
        # List to hold count of each suit pile
        self.suit_piles_count = [0, 0, 0, 0]  # S H C D     
        # a list for transfering card objects between different place
        self.transfer_list = []
        # Place all cards into the corresponding slots 
        self._init_cards()
        
    def _init_cards(self):
        # Shuffle the deck of cards
        self._game_deck.shuffle()
        
        # Place all cards into the matrices
        self.down_deck_matrix = [
            [],
            [self._game_deck.deck[7]],
            self._game_deck.deck[8:10],
            self._game_deck.deck[10:13],
            self._game_deck.deck[13:17],
            self._game_deck.deck[17:22],
            self._game_deck.deck[22:28]
            ]
            
        self.up_deck_matrix = [
            [self._game_deck.deck[0]],
            [self._game_deck.deck[1]],
            [self._game_deck.deck[2]],
            [self._game_deck.deck[3]],
            [self._game_deck.deck[4]],
            [self._game_deck.deck[5]],
            [self._game_deck.deck[6]]
            ]
        
        self.down_left_corner_deck = self._game_deck.deck[28:52]
        
        
    def check_for_win(self) -> bool:
        """Returns 'True' if game has been won, 'False' if not"""
        for suit_count in self.suit_piles_count:
            if suit_count != 13:
                return False        
        return True
        
    def add_to_matrix(self, add_loc, add_list: list):
        """
        Modify matrices 
        :param int add_num: number of cards you want to add
        :param int add_loc: index to add to
        """
        for i in add_list:
            self.up_deck_matrix[add_loc].append(i)
    
    def bottom_to_top(self):
        for i in range(len(self.up_deck_matrix)):
            if len(self.up_deck_matrix[i]) == 0 and len(self.down_deck_matrix[i]) != 0:
                self.up_deck_matrix[i].append(self.down_deck_matrix[i].pop())
            
                
    def remove_from_matrix(self, remove_num: int, remove_loc: int) -> list:
        """
        Modify matrices 
        :param int remove_num: number of cards y ou want to remove
        :param int remove_loc: index to remove from
        """
        return_list = []
        
        for i in range(remove_num):
            return_list.append(self.up_deck_matrix[remove_loc].pop())  
        
        
        
        return return_list
    
