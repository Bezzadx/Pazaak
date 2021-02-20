from pazaak_hand import *


class board():
    def __init__(self, players, hands, starting_scores = (0,0), starting_turn = 1, match_score = (0, 0)):
        self.players = players
        self.hands = hands
        self.scores = list(starting_scores)
        self.turn = starting_turn
        self.match_score = list(match_score)
        self.stick = [False, False]
        self.cards_played = [[],[]]
        
        #TODO: implement move recorder from which agents can make inferences about opponent cards

    def __str__(self):
        return str(self.players[0]) + " " + str(self.scores[0]) + " : " + str(self.scores[1]) + " " + str(self.players[1])
    
    def __repr__(self):
        first_line = "Players are " + str(self.players[0]) + " and " + str(self.players[1]) + "\n"
        second_line = "The round score is " + str(self.scores) + "\n"
        third_line = str(self.players[0]) + " holds " + str(self.hands[0]) + "\n"
        fourth_line = str(self.players[0]) + " holds " + str(self.hands[0]) + "\n"
        fifth_line = str(self.players[self.turn]) + " to play."
        return first_line + second_line + third_line + fourth_line + fifth_line
    
    #Reset the game board for a new round
    def reset(self):
        self.scores = [0, 0]
        self.stick = [False, False]
    
    def other_player(self, player):
        return (player + 1) % 2
    
    def switch_player(self):
        self.turn = self.other_player(self.turn)
    
    
    #When a card is played, adds it to the player's total, and removes it from their hand
    def move(self, card):
        if not self.hands[self.turn].check([card]):
            pass
        else:
            self.scores[self.turn] += card
            self.hands[self.turn].remove(card)
    
    
    #Same as other_player, but taking and returning player instances instead of numbers
    def opponent(self, player):
        if player == self.players[0]:
            return self.players[1]
        elif player == self.players[1]:
            return self.players[0]
        else:
            return None
    
    def available_actions(self):
        actions = {0}
        for card in self.hands[self.turn]:
            actions.add(card)
            
        return actions