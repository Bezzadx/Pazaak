from dice import *
from pazaak_play_game import *
from pazaak_game_board import *
from pazaak_hand import *

def performance(bot0, bot1, n):
    #initialize score tracker
    score = {bot0: 0, bot1: 0}
    
    for i in range(n):
        #initialize hands
        players = [bot0, bot1]
        players[0] = bot0
        players[1] = bot1
        
        rolls = (rolln(6, 1, 4), rolln(6, 1, 4))
        
        hand0 = hand(rolls[0])
        hand1 = hand(rolls[1])
    
        hands = [hand0, hand1]

        #create game board
        game = board(players, hands)
        for x in [0, 1]:
            players[x].board = game
            players[x].order = x
            players[x].assign(hands[x])

        #Play rounds until one player wins 3.
        while game.match_score[0] != 3 and game.match_score[1] != 3:
            round_winner = play_test_round(game)
        
            if round_winner != None:
                game.match_score[round_winner] += 1
            
        #increment score tracker depending on winner
        if game.match_score[0] == 3:
            score[game.players[0]] += 1
        else:
            score[game.players[1]] += 1
    
    return score
    


def play_test_round(game):
    winner = None
    
    while True:
        """Play one full turn"""
        
        #Step 0: switch player
        game.switch_player()
        
        #Step 1: Draw card and add to round score
        card = roll(10)        
        game.scores[game.turn] += card

        #Step 2: Ask player for move
        player_move = game.players[game.turn].move()
        
        card = game.hands[game.turn].remove(player_move[0])
        
        if card != 0:
            game.cards_played[game.turn].append(card)
            game.scores[game.turn] += card
        
        game.stick[game.turn] = player_move[1]

        #Step 3: check win conditions
        if game.scores[game.turn] > 20:
            winner = game.other_player(game.turn)
            break
        
        elif all(game.stick):
            if game.scores[0] > game.scores[1]:
                winner = 0
                break
            
            elif game.scores[1] > game.scores[0]:
                winner = 1
                break
            
            else:
                break

        #Step 4: end turn
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
