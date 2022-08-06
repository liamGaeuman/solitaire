from tkinter import *
import cards
from SolitaireGame import SolitaireGame

class SolitaireDisplay(Canvas):
    
    def __init__(self, master, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.master = master
        
        #create window title
        master.title("Solitaire")
        #set image for back of card
        self.backImage = PhotoImage(file="DECK/b.gif")
        #draw board
        self._draw_board()
        #initialize game object
        self.game = None
        
        
        
        #bottom 7 upward facing card objects matrix
        self.card_imgs = [[],[],[],[],[],[],[]] 
        #bottom 7 upward image objects matrix
        self.imgs = [[],[],[],[],[],[],[]]
        #list of card images for bottom deck
        self.garbage_card_imgs = [] #need?
        
        
        #self.currentCard = None  #?
        self.currentCardImage = None  #array can be used likely
        self.initial_click = None #need this
        self.win_stack_imgs = [None,None,None,None]  #Need!
        
        #create a new solitaire game
        self._new_game()
 
    def _new_game(self):
        #create a new solitaire game
        self.game = SolitaireGame()
        #update the cards
        self._update_cards_display()
        #create corner cards 
        self._left_corner_deck()
  
    def _left_corner_deck(self):
        #This function builds the left corner game deck and it's functionality
        #create deck reset click listener
        self.tag_bind("rectDeck","<Button-1>", self._reset_rect_deck)
        #create look of left corner deck
        self._rect_deck_cards()
        #create deck flipper click listener
        self.tag_bind("flipper","<Button-1>", self.flip)
    
    def _rect_deck_cards(self):
        #This function adds the cards from the looked at deck back to the main corner deck
        self.cornerCards = []
        if len(self.game.down_left_corner_deck) < 5:
            count = len(self.game.down_left_corner_deck)
        else:
            count = 5
        x, y = 16, 16
        for i in range(count):  
            card = self.create_image(x,y, anchor=NW, image=self.backImage, tag="flipper")
            self.cornerCards.append(card)
            x += 2
            y += 2
    
    def _reset_rect_deck(self, event):
        #This function resets all the cards in the left corner deck"""
        #reverse the cards before you put them back
        self.game.up_left_corner_deck.reverse()
        self.game.down_left_corner_deck.extend(self.game.up_left_corner_deck[::])
        self.game.up_left_corner_deck = []
        self._rect_deck_cards()
        #check that you are not deleting it even if it has been dragged away and used
        try:
            self.delete(self.currentCardImage)
        except AttributeError:
            pass
    
    def flip(self, event):
        """This function makes the cards move from corner deck to already looked at deck"""
        #if deck length is less than five, show it visually
        if len(self.game.down_left_corner_deck) <= 5:
            card = self.cornerCards.pop()
            #delete card from stack
            self.delete(card)
        #remove card image after the next one is introduced
        try:
            self.delete(self.currentCardImage)
        except AttributeError:
            pass
            
        self.game.transfer_list.clear()
        
        self.game.transfer_list.append(self.game.down_left_corner_deck.pop())#assign current card to currentCard variable
        #create image card
        self.ImageOfCurrentCard = PhotoImage(file="DECK/" + self.game.transfer_list[0].image())
        self.currentCardImage = self.create_image(120, 16,
                anchor=NW, image=self.ImageOfCurrentCard, tag="dragMe")
        self.game.up_left_corner_deck.append(self.game.transfer_list[0])
        #if card is dragged pop it and call a function to add it to its new home
        self.tag_bind("dragMe", "<Button-1>", self.drag_start)
        self.tag_bind("dragMe", "<B1-Motion>", self.drag_motion)
        self.tag_bind("dragMe", "<ButtonRelease-1>",self.onRelease)
  
    def drag_start(self, event):
        self.initial_click = event.x, event.y
        self.click = event.x, event.y  
        self.tag_raise('current')
        self.xy = self._get_matrix_location(self.initial_click)
        
        if self.xy != None:
            self.game.transfer_list = self.game.remove_from_matrix(len(self.game.up_deck_matrix[self.xy[0]])-self.xy[1],self.xy[0])
            print(self.game.transfer_list)
            
    def drag_motion_bottom_cards(self, event):   #ditch this boi
        x, y = self.click 
        dx = event.x - x
        dy = event.y - y        
        #self.move('current',dx,dy)
        
        #move the other cars too!
        
        if self.xy != None:
            for i in range(self.xy[1],len(self.card_imgs[self.xy[0]])):
                #print(i)
                self.move(self.card_imgs[self.xy[0]][i],dx,dy)
                
        self.click = event.x, event.y
        
    def drag_motion(self, event):
        x, y = self.click
        self.coords('current' ,x-36 ,y-15)
        self.click = event.x, event.y

    def _get_matrix_location(self, click: tuple) -> tuple:       
        #if (x := self._get_card_orgin()-1) == -1:
        x = self._get_card_orgin(click)-1
        if x == -1:
            return None
        #starting height of up cards
        s = len(self.game.down_deck_matrix[x]) * 8 + 129
        #vertical distance between start of up cards and click
        z = self.initial_click[1] - s
        #get y index of clicked card
        y = (z//30)
        if z % 30 != 0:
            y+=1 
        if y > len(self.game.up_deck_matrix[x]):
            y = len(self.game.up_deck_matrix[x])
        y-=1 #make it an index          
        return(x,y)
        
    def _get_pile(self, click: tuple) -> int:
        if click[1] <= 113 and click[1] >= 16:
            if click[0] >= 283 and click[0] <= 356:
                return 0
            if click[0] >= 372 and click[0] <= 445:
                return 1
            if click[0] >= 461 and click[0] <= 534:
                return 2
            if click[0] >= 550 and click[0] <= 623:
                return 3
        return None
    
    def _check_suit(self, pile: int) -> bool:
        print(self.game.transfer_list[0].suit)
        if pile == 0:
            if self.game.transfer_list[0].suit == "Spades":
                return True    
        if pile == 1:
            if self.game.transfer_list[0].suit == "Hearts":
                return True     
        if pile == 2:
            if self.game.transfer_list[0].suit == "Clubs":
                return True     
        if pile == 3:
            if self.game.transfer_list[0].suit == "Diamonds":
                return True
        return False    
    
    def _check_rank(self, pile: int)-> bool:
        if self.game.suit_piles_count[pile] == self.game.transfer_list[0].rank-1:
            return True
        return False
    
    def _get_card_orgin(self, click: tuple) -> int:
        if click[1] <= 113 and click[1] >= 16:
            return 0 
        if click[1] >= 129:
            if click[0] <= 89 and click[0] >= 16:
                return 1 
            if click[0] <= 178 and click[0] >= 16:
                return 2
            if click[0] <= 267 and click[0] >= 105:
                return 3
            if click[0] <= 356 and click[0] >= 283:
                return 4
            if click[0] <= 445 and click[0] >= 372:
                return 5
            if click[0] <= 534 and click[0] >= 461:
                return 6
            if click[0] <= 623 and click[0] >= 550:
                return 7
        return None
    
    def _remove_card(self, num: int):       
        if num == 0:
            print(self.game.up_left_corner_deck.pop())
        else:
            print(self.game.transfer_list.pop())
    
    def onRelease(self, event):
        click_result = self._get_pile(self.click) 
        # drop card over top 4 piles 
        if click_result != None and len(self.game.transfer_list) == 1: #check transfer list equaling 1 good           
            if self._check_suit(click_result):               
                if self._check_rank(click_result):                   
                    self.game.suit_piles_count[click_result] += 1 
                    if self._get_card_orgin(self.initial_click) == 0:
                        print(self.ImageOfCurrentCard)
                        self.win_stack_imgs[click_result] = self.ImageOfCurrentCard
                        self.delete(self.currentCardImage)
                    else:
                        
                        #access the image matrix element 
                        xy = self._get_matrix_location(self.initial_click)
                        print(self.card_imgs[xy[0]][xy[1]])
                        self.win_stack_imgs[click_result] = self.imgs[xy[0]][xy[1]]
                        
                    
                    self._remove_card(self._get_card_orgin(self.initial_click)) #good up to here
                    
                    self.create_image(283 + click_result * 89,
                        16,
                        anchor=NW,
                        image=self.win_stack_imgs[click_result]
                        )
        else:
            # move portion of stack to another stack
            # check release point is one of the stacks
            card_org = self._get_card_orgin(self.click) #release not click #create a procedure for cards that come from 0 pile
            
            if (card_org != None and card_org != 0):
                #check suite and rank against top stack card
                
                if self._black_and_red(self.game.transfer_list[0],self.game.up_deck_matrix[card_org]):
                    #if self.game.transfer_list[0].rank()-1 == self.game.up_deck_matrix[card_org].rank():
                    self.game.transfer_list.reverse()
                    self.game.add_to_matrix(self._get_card_orgin(self.click)-1, self.game.transfer_list)
                    #clear the transfer list after it has been added to another stack
                    self.game.transfer_list.clear()
        
       
        #move the card back if it doesn't work  
        self._put_card_back()
        
        self._update_cards_display()
        
        if self.game.check_for_win():
            print("you win!")
    
    def _black_and_red(self, card1, card2) -> bool:
        return True
    
    def _put_card_back(self):
        if self._get_card_orgin(self.initial_click) == 0:
            self.moveto('current', 120, 16)  
        else:
            xy = self._get_matrix_location(self.initial_click) 
            self.game.add_to_matrix(xy[0],self.game.transfer_list)
            self.game.transfer_list.clear()
            #self.delete(self.card_imgs[xy[0]][xy[1]])
   
    def _update_cards_display(self):
        #clear card canvas image objects from bottom row
        self.game.bottom_to_top()
        for i in self.garbage_card_imgs:
            self.delete(i)   
        #displays contents of matrices 
        #draw downward facing cards
        x = 16
        y = 129        
        for cards in self.game.down_deck_matrix:  
            for card in cards:                      
                self.garbage_card_imgs.append(self.create_image(x,
                    y,
                    anchor=NW,
                    image=self.backImage,
                   ))
                y+=8
            y=129
            x += 89
        #draw upward facing cards
        for cards in self.card_imgs:
            for card in cards:
                self.delete(card) 
        for cards in self.imgs:
            for card in cards:
                self.delete(card) 
        x = 16
        count = 0
        for cards in self.game.up_deck_matrix:
            y = (129  
                + 8
                * len(self.game.down_deck_matrix[count])
                )   
            count += 1
            for card in cards:
                card_img = PhotoImage(file="DECK/" + card.image())
                self.imgs[count-1].append(card_img)
                
                self.card_imgs[count-1].append(self.create_image(x,
                    y,
                    anchor=NW,
                    image=card_img,
                    tag="bottomCards"
                   ))
                y+=30
            x += 89
        self.tag_bind("bottomCards", "<Button-1>", self.drag_start)
        self.tag_bind("bottomCards", "<B1-Motion>", self.drag_motion_bottom_cards)
        self.tag_bind("bottomCards", "<ButtonRelease-1>",self.onRelease)
  
    def _draw_board(self):
        #Draw rectangles for cards to sit in
        self.create_rectangle(16, 16, 89, 113, fill="red4", tag="rectDeck")  
        self.create_rectangle(283, 16, 356, 113)
        self.create_rectangle(372, 16, 445, 113)
        self.create_rectangle(461, 16, 534, 113)
        self.create_rectangle(550, 16, 623, 113)
        self.create_rectangle(16, 129, 89, 227)
        self.create_rectangle(105, 129, 178, 227)
        self.create_rectangle(194, 129, 267, 227)
        self.create_rectangle(283, 129, 356, 227)
        self.create_rectangle(372, 129, 445, 227)
        self.create_rectangle(461, 129, 534, 227)
        self.create_rectangle(550, 129, 623, 227)
    
def main():
    root = Tk()
    game = SolitaireDisplay(root, width=639, height=500, bg="red4") 
    game.pack()
    root.mainloop()
    
if __name__ == "__main__":
    main()
      