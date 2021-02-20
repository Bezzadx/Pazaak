from dice import *
from pazaak_play_game import *
from pazaak_game_board import *
from pazaak_hand import *
from pazaak_ai import *
import random as r

#Training parameters
REPETITIONS = 50000
TIME_DECAY = 0.9
Q_REWARD = 1
EXPLORATION_RATE = 0.4


def train(n = REPETITIONS):
    #initialize two agents that share the same q-learning dictionary
    bot0 = AI(q_values = dict())
    bot1 = AI(q_values = dict(), name = "R2-D2")
    Q = dict()
    bot0.q_values = Q
    bot0.order = 0
    
    bot1.q_values = Q
    bot1.order = 1
    
    players = [bot0, bot1]
    players[0] = bot0
    players[1] = bot1
    
    for i in range(n):
        #initialize hands
        rolls = (rolln(6, 1, 4), rolln(6, 1, 4))
        
        hand0 = hand(rolls[0])
        hand1 = hand(rolls[1])
        
        hands = [hand0, hand1]
    
        #create game board
        game = board(players, hands)
        for x in [0, 1]:
            players[x].board = game
            players[x].assign(hands[x]) 

        
        #Play 5 rounds
        for j in range(5):
            round_winner = play_training_round(game)
            
            if round_winner != None:
                game.match_score[round_winner] += 1
    
    return bot0


def play_training_round(game):
    actions = {0: dict(), 1: dict()}
    winner = None
    
    while True:
        """play one full turn"""
        #step 0: Switch player
        game.switch_player()
        
        #step 1: Draw card and add to round score
        card = roll(10)        
        game.scores[game.turn] += card
        
        #Step 2: Ask player for move
        player_move = game.players[game.turn].move()
        
        card = game.hands[game.turn].remove(player_move[0])
        
        if card != 0:
            game.cards_played[game.turn].append(card)
            game.scores[game.turn] += card
        
        #Step2.1: With probability EXPLORATION_RATE, randomly choose to Stick/Twist instead of the agent's decision.
        x = r.uniform(0,1)
        if x > EXPLORATION_RATE:
            game.stick[game.turn] = player_move[1]
        else:
            game.stick[game.turn] = r.choice([True, False])
        
        #Step 2.2: Update actions to reflect this move
        for action in actions[game.turn]:
            actions[game.turn][action] *= TIME_DECAY
        
        actions[game.turn][(game.players[game.turn].get_state(), game.stick[game.turn])] = 1
        
        #Step 3: Check win conditions and update q_values appropriately
        
        #Check for bust
        if game.scores[game.turn] > 20:
            winner = game.other_player(game.turn)
            for pair in actions[winner]:
                game.players[winner].update_q(pair, Q_REWARD * actions[winner][pair])
            
            for pair in actions[1 - winner]:
                game.players[1 - winner].update_q(pair, -(Q_REWARD * actions[1 - winner][pair]))
                
            break
        
        #If both players have stuck, check for high score
        elif all(game.stick):
            if game.scores[0] > game.scores[1]:
                winner = 0
                
                for pair in actions[winner]:
                    game.players[winner].update_q(pair, Q_REWARD * actions[winner][pair])
            
                for pair in actions[1 - winner]:
                    game.players[1 - winner].update_q(pair, -(Q_REWARD * actions[1 - winner][pair]))
            
                break
            
            elif game.scores[1] > game.scores[0]:
                winner = 1
                
                for pair in actions[winner]:
                    game.players[winner].update_q(pair, Q_REWARD * actions[winner][pair])
            
                for pair in actions[1 - winner]:
                    game.players[1 - winner].update_q(pair, -(Q_REWARD * actions[1 - winner][pair]))
            
                break
            
            else:
                for pair in actions[0]:
                    game.players[0].update_q(pair, 0)
                
                for pair in actions[1]:
                    game.players[1].update_q(pair, 0)
                break

        #Step 4: End turn
        if game.stick[game.other_player(game.turn)]:
            """
            NB: This 'pre-switches' the players as the players are always switched
            at the start of each cycle
            """
            game.switch_player()
            continue
        else:
            
            continue
            
    
    game.reset()
    return winner



def Q_REWARD_function(board, player = 0, reward = Q_REWARD):
    #placeholder
    return reward

