from dice import *
from pazaak_play_game import *
from pazaak_game_board import *
from pazaak_hand import *
from pazaak_bot import *
from copy import deepcopy

BSIMULATIONS = 150
CARD_COST = 0.6

class bot_plus():
    def __init__(self, name = "R2-D2", simulations = BSIMULATIONS):
        
        self.name = str(name)
        self.board = None
        self.order = None
        
        self.sims = simulations
        self.agent0 = bot(name = "agent0")
        self.agent1 = bot(name = "agent1")
    
        
    
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    
    def assign(self, HAND):
        HAND.cards[2] = - HAND.cards[2]
        HAND.cards[3] = - HAND.cards[3]
        
        self.board.hands[self.order] = HAND
    
    def move(self):
        
        if self.board.scores[self.order] < 12:
            return [0, False]
        
        candidates = self.monte_carlo_search()

        for action in candidates:
            if action[0] != 0:
                candidates[action] -= self.sims * CARD_COST
        
        best_value = max(candidates.values())
        for action in candidates:
            if candidates[action] == best_value:
                return action
        return [0, False]
    
    def monte_carlo_search(self):
        candidates = {(0, True): 0, (0, False): 0}
        
        for card in self.board.hands[self.order].cards:
            if self.board.scores[self.order] + card <= 20:
                candidates[(card, True)] = 0
                candidates[(card, False)] = 0
        
        for action in candidates:
            for i in range(self.sims):
                candidates[action] += self.rollout(action, self.agent0, self.agent1)
        
        return candidates

    
    def simulate_hand(self):
        cards = []
        cards_played = self.board.cards_played[1 - self.order]
        positives = 2
        negatives = 2
        for card in cards_played:
            if card < 0:
                negatives -= 1
            elif card > 0:
                positives -= 1
        
        for i in range(positives):
            cards.append(roll(6))
        for i in range(negatives):
            cards.append(roll(6))
        
        return hand(cards)
    
    def rollout(self, action, agent0, agent1):
        
        #Create duplicate board
        opponent_hand = self.simulate_hand()
        clone = board([agent0, agent1], [deepcopy(self.board.hands[self.order]), opponent_hand])
        
        clone.scores[0] = self.board.scores[self.order] + action[0]
        clone.scores[1] = deepcopy(self.board.scores[1 - self.order])
        
        clone.stick[0] = action[1]
        clone.stick[1] = deepcopy(self.board.stick[1 - self.order])
        
        clone.cards_played[0] = deepcopy(self.board.cards_played[self.order])
        clone.cards_played[1] = deepcopy(self.board.cards_played[1 - self.order])
        if action[0] != 0:
            clone.cards_played[0].append(clone.hands[0].remove(action[0]))
        
        
        agent0.board = clone
        agent0.order = 0
        agent1.board = clone
        agent1.order = 1
        
        clone.turn = 0
        
        #Play out round from this position
        
        while True:
            """Complete one full turn"""
            
            #Step 0: check win conditions
            
            #Check bust
            if clone.scores[clone.turn] > 20:
                winner = clone.other_player(clone.turn)
                break
        
            #If both players have stuck, check high scores
            elif all(clone.stick):
                if clone.scores[0] > clone.scores[1]:
                    winner = 0
                    break
                elif clone.scores[0] < clone.scores[1]:
                    winner = 1
                    break
                else:
                    winner = None
                    break
        
            #Step 1: Determine next to play 
            if clone.stick[clone.other_player(clone.turn)]:
                pass
            else:
                clone.switch_player()
                pass
        
            #Step 2: Draw card and add to round scores
            card = roll(10)
            clone.scores[clone.turn] += card
        
            #Step 3: Ask player for their move
            player_move = clone.players[clone.turn].move()
            card = clone.hands[clone.turn].remove(player_move[0])
            
            if card != 0:
                clone.cards_played[clone.turn].append(card)
                clone.scores[clone.turn] += card
        
            clone.stick[clone.turn] = player_move[1]
        
        if winner == 0:
            return 1
        elif winner == 1:
            return -1
        else:
            return 0
        
         
    
    