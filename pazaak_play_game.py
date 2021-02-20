from pazaak_play_round import *
from pazaak_game_board import *
from time import sleep

def play(player0, player1, play_to = 3):

    #Initialize hands
    players = [player0, player1]
    rolls = (rolln(6, 1, 4), rolln(6, 1, 4))
    hand0 = hand(rolls[0])
    hand1 = hand(rolls[1])
    

    hands = [hand0, hand1]
    
    #create game board
    game = board(players, hands)
    for i in [0, 1]:
        players[i].board = game
        players[i].order = i
        players[i].assign(hands[i])
    
    #play rounds until one player reaches play_to score
    while game.match_score[0] != play_to and game.match_score[1] != play_to:
    #while True:
        #Announce current match score
        print(f"\nThe match score is {players[0]} {game.match_score[0]} : {game.match_score[1]} {players[1]}")
        sleep(1)
        
        #determine the winner of a round
        round_winner = play_round(game)
        
        if round_winner != None:
            game.match_score[round_winner] += 1
        

    
    print(f"Final Score: {game.players[0]} {game.match_score[0]} : {game.match_score[1]} {game.players[1]}")
