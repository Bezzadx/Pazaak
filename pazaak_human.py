from dice import *
from pazaak_play_game import *
from pazaak_game_board import *
from pazaak_hand import *
from pazaak_interface_tools import *


class human():
    def __init__(self, name = "Han"):
        
        self.name = str(name)
        self.board = None
        self.order = None
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def assign(self, HAND):
        while True:
            print("Deck: " + str(HAND))
            x = get_int("select first positive card: ", sign = 1)
            y = get_int("select second positive card: ", sign = 1)
            
            if HAND.check([x, y]):
                indices = HAND.get_indices([x,y])
                
                dummy = hand([])
                
                for i in range(4):
                    if i in indices:
                        dummy.cards.append(HAND.cards[i])
                    else:
                        dummy.cards.append( - HAND.cards[i])
                
                
                if get_bool("Do you want to use " + str(dummy) + " as your deck? (y/n) \n"):
                    self.board.hands[self.order] = dummy
                    break
                else:
                    print("Reassigning...\n")
                    continue
            
            print("You don't hold those cards.\n")
    
    def move(self):
        card = self.play_card()
        stick = self.stick()
        
        return [card, stick]
    
    def play_card(self):
        print(f"Available Cards: {Fore.CYAN}{self.board.hands[self.order]}{Style.RESET_ALL}\n")
        
        while True:
            card = get_int("Select a card or enter 0 if you do not wish to play a card: ", sign = 0)
            
            if self.board.hands[self.order].check([card]) or card == 0:
                return card
            
            else:
                print("You are not holding that card")
    
    
    def stick(self):
        answer = get_bool("Would you like to stick?\n")
        return answer


han = human()
greedo = human(name = 'Greedo')