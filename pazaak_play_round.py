from time import sleep  
from dice import *
from pazaak_play_game import *
from pazaak_game_board import *
from pazaak_hand import *
from colorama import Fore
from colorama import Style
from colorama import init as colorama_init

colours = {0: Fore.GREEN, 1: Fore.YELLOW, 2: Fore.RED, 3: Fore.CYAN}
"""
Takes a board object as an input, then plays out that round, 
returning the winner of the round, or None if there is no winner
"""
def play_round(game):
    winner = None
    
    while True:
        """Play one full turn"""
        
        #Step 0: switch player
        game.switch_player()
        print(f"\n{colours[game.turn]}{game.players[game.turn]} to play{Style.RESET_ALL}\n")
        
        #Step 1: draw card and add to round score
        print("Drawing...")
        sleep(0.5)
        
        card = roll(10)        
        game.scores[game.turn] += card
        
        print(f"{colours[2]}Card: {card}{Style.RESET_ALL}\nScore: {colours[game.turn]}{game.scores[game.turn]}{Style.RESET_ALL} : {colours[game.other_player(game.turn)]}{game.scores[game.other_player(game.turn)]}{Style.RESET_ALL}")
        
        #Step 2: ask the player for their move
        if game.stick[game.other_player(game.turn)]:
            print(f"{colours[game.other_player(game.turn)]}{game.players[game.other_player(game.turn)]}{Style.RESET_ALL} has stuck on {colours[game.other_player(game.turn)]}{game.scores[game.other_player(game.turn)]}{Style.RESET_ALL}.")
        else:
            print(f"{colours[game.other_player(game.turn)]}{game.players[game.other_player(game.turn)]}{Style.RESET_ALL} twisted on {colours[game.other_player(game.turn)]}{game.scores[game.other_player(game.turn)]}{Style.RESET_ALL}.")
        
        player_move = game.players[game.turn].move()
        
        card = game.hands[game.turn].remove(player_move[0])
        
        if card != 0:
            game.cards_played[game.turn].append(card)
            game.scores[game.turn] += card
        
        game.stick[game.turn] = player_move[1]
        
        if player_move[0] and player_move[1]:
            print(f"{colours[game.turn]}{game.players[game.turn]}{Style.RESET_ALL} plays {colours[game.turn]}{card}{Style.RESET_ALL} and sticks.\n")
        elif player_move[0]:
            print(f"{colours[game.turn]}{game.players[game.turn]}{Style.RESET_ALL} plays {colours[game.turn]}{card}{Style.RESET_ALL} and twists.\n")
        elif player_move[1]:
            print(f"{colours[game.turn]}{game.players[game.turn]}{Style.RESET_ALL} does {colours[3]}not{Style.RESET_ALL} play a card, and sticks.\n")
        else:
            print(f"{colours[game.turn]}{game.players[game.turn]}{Style.RESET_ALL} does {colours[3]}not{Style.RESET_ALL} play a card, and twists.\n")
        
        #Step 3: check win conditions
        
        #Check bust
        if game.scores[game.turn] > 20:
            print(f"{colours[game.turn]}{game.players[game.turn]}{Style.RESET_ALL} is bust.")
            winner = game.other_player(game.turn)
            break
        
        #If both players have stuck, check for high score
        elif all(game.stick):
            if game.scores[0] > game.scores[1]:
                print(f"{colours[0]}{game.players[0]}{Style.RESET_ALL} has the high score.")
                winner = 0
                break
            
            elif game.scores[1] > game.scores[0]:
                print(f"{colours[1]}{game.players[1]}{Style.RESET_ALL} has the high score.")
                winner = 1
                break
            
            else:
                print(f"Scores are {colours[3]}tied{Style.RESET_ALL}")
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