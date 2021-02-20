from dice import *
from pazaak_play_game import *
from pazaak_game_board import *
from pazaak_hand import *
from q_values import Q_VALUES

REWARD = 1
PENALTY = -1
CARD_COST = 0.6

class AI():
    
    def __init__(self, name = "T3-M4", q_values = Q_VALUES):
        
        self.name = str(name)
        self.board = None
        self.order = None
        
        self.q_values = q_values
        
        #Represent beliefs about opponent's hand (currently unused)
        self.memory = None
        self.knowledge = dict()
        self.knowledge["positive"] = {1,2,3,4,5,6}
        self.knowledge["negative"] = {1,2,3,4,5,6}
        
        #Counts how many positive and negative cards the opponent has played (currently unused)
        self.card_counter = [0, 0]
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    
    def assign(self, HAND):
        #placeholder
        HAND.cards[2] = - HAND.cards[2]
        HAND.cards[3] = - HAND.cards[3]
        
        self.board.hands[self.order] = HAND
    
    def move(self):
        self.update_knowledge()
        
        #Search for statistical best move if opponent has stuck. Could be re-written more elegantly using evaluate method
        if self.board.stick[self.board.other_player(self.order)]:
            
            best_stick_score = self.best_score(self.board.hands[self.order])
            
            if (self.board.scores[self.order] % 21) > self.board.scores[1 - self.order]:
                stick_value = REWARD
                stick_card = 0
            elif best_stick_score > self.board.scores[1 - self.order]:
                stick_value = REWARD - CARD_COST
                stick_card = best_stick_score - self.board.scores[self.order]
            elif self.board.scores[self.order] == self.board.scores[1 - self.order]:
                stick_value = 0
                stick_card = 0
            elif best_stick_score == self.board.scores[1 - self.order]:
                stick_value = -CARD_COST
                stick_card = best_stick_score - self.board.scores[self.order]
            else:
                stick_value = PENALTY
                stick_card = 0
        
            expected_twist_value = 0
            
            for draw in range(1,11):
                new_total = self.board.scores[self.order] + draw
                best_new_score = self.best_score(self.board.hands[self.order], DRAW = draw)
                
                if new_total % 21 > self.board.scores[1 - self.order]:
                    draw_value = REWARD
                elif best_new_score > self.board.scores[1 - self.order]:
                    draw_value = REWARD - CARD_COST
                elif new_total  == self.board.scores[1 - self.order]:
                    draw_value = 0
                elif best_new_score == self.board.scores[1 - self.order]:
                    draw_value = -CARD_COST
                else:
                    draw_value = PENALTY
                
                expected_twist_value += draw_value
            
            expected_twist_value /= 10
            
            if expected_twist_value > stick_value:
                return [0, False]
            elif expected_twist_value < stick_value:
                return [stick_card, True]
            else:
                return [0, False]
        
        #Evaluate all candidate moves using the evaluate function, which has been trained with q-learning
        else:
            candidate_moves = [(self.evaluate(self.get_state(), False), [0, False]), (self.evaluate(self.get_state(), True), [0, True])]
            
            for card in self.board.hands[self.order].cards:
                candidate_moves.append((self.evaluate(self.get_state(card), False) - CARD_COST, [card, False]))
                candidate_moves.append((self.evaluate(self.get_state(card), True) - CARD_COST, [card, True]))            

            return sorted(candidate_moves)[-1][1]
            
            


    #Calculates the best score possible by playing a card from HAND, with a given starting score and a possible drawn card.
    def best_score(self, HAND, current_score = None, DRAW = 0):
        if current_score == None:
            score = self.board.scores[self.order] + DRAW
        else:
            score = current_score + DRAW
        
        candidate = bust(score)
        
        for card in HAND.cards:
            if bust(score + card) > candidate:
                candidate = score + card
        
        return candidate
    
    
    #Returns the current board state from the current player's perspective. Can optionally be used to return the board state after a card has been placed by either player, or both.
    def get_state(self, own_card = 0, opponent_card = 0):
        a = self.board.scores[self.order] + own_card
        b = self.board.scores[1 - self.order] + opponent_card
        c = self.board.stick[1 - self.order]
        d = not bool(self.board.cards_played[1 - self.order])
        return(a, b, c, d)
    
    #Returns the q-value for a given state/action pair, where actions are represented by True for 'stick' and False for 'twist'.
    def get_q_value(self, state, action):
        pair = (state, action)
        
        if pair in self.q_values:
            return self.q_values[pair][0]
        
        else:
            return 0

    #Returns the evaluation of a given state/action pair, effectively giving the win rate of the action in the given state.
    def evaluate(self, state, action):
        pair = (state, action)
        if pair in self.q_values:
            return self.q_values[pair][0] / self.q_values[pair][1]
        else:
            return 0
    
    
    #Update q-value for a given state/action pair, and tracks how many times this pair has appeared in training
    def update_q(self, state_action, reward):
        if state_action in self.q_values:
            self.q_values[state_action][0] += reward
            self.q_values[state_action][1] += 1
        else:
            self.q_values[state_action] = [reward, 1]

    
    #placeholder
    def update_knowledge(self):
        self.memory = self.board.cards_played[1 - self.order]
            
    

#helper function for best_score method
def bust(score):
    if score > 20:
        return 0
    else:
        return score