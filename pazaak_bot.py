from dice import *
from pazaak_play_game import *
from pazaak_game_board import *
from pazaak_hand import *



class bot():
    def __init__(self, name = "C3-PO"):
        
        self.name = str(name)
        self.board = None
        self.order = None
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    
    def assign(self, HAND):
        HAND.cards[2] = - HAND.cards[2]
        HAND.cards[3] = - HAND.cards[3]
        
        self.board.hands[self.order] = HAND
    
    def move(self):
        #Establish target range
        if self.board.stick[1 - self.order]:
            target_range = range(self.board.scores[1 - self.order], 21)
        
        else:
            target_range = range(18,21)
        
        if self.board.scores[self.order] in target_range:
            return [0, True]
        
        else:
            candidate_actions = set()
            
            #Loop through available cards, looking for candidate moves
            for card in self.board.hands[self.order].cards:
                if (self.board.scores[self.order] + card) in target_range:
                    candidate_actions.add(card)
            
            if candidate_actions and self.board.stick[1 - self.order]:
                best_card = min(candidate_actions)
                return [best_card, True]
            
            elif candidate_actions:
                best_card = max(candidate_actions)
                return [best_card, True]
            
            else:
                return [0, False]
    
C3_PO = bot()

            
        