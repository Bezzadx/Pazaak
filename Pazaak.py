import math
import time
from dice import *
import Helper_Functions as h 

class Deck():
    def __init__(self, cards = None):
        if isinstance(cards, list) and all(isinstance(card, int) for card in cards):
            self.cards = cards
        else:
            self.cards = [roll(6), roll(6), roll(6), roll(6)]
    
    def __str__(self):
        dummy = [card for card in self.cards if card != None] 
        return str(dummy)
    
    def __repr__(self):
        dummy = [card for card in self.cards if card != none] 
        return str(dummy)
        
    def check(self, check_cards = []):
        for card in self.cards:
            for i in range(len(check_cards)):
                if card == check_cards[i]:
                    check_cards[i] = None
                    break
        return all(card == None for card in check_cards)
   
    def get_indices(self, get_cards = []):
        indices = [None for card in get_cards]
        
        for i in range(len(self.cards)):
            for j in range(len(get_cards)):
                if self.cards[i] == get_cards[j] and self.cards[i] != None:
                    indices[j] = i
                    get_cards[j] = None
                    break
        
        return indices
        
    def get_length(self):
        counter = 0
        for card in self.cards:
            if card:
                counter += 1
        
        return counter

class human():
    def __init__(self, name = "Greedo", hand = Deck()):
        if isinstance(name, str):
            self.name = name
        else:
            self.name = str(name)
        
        if isinstance(hand, Deck) and len(hand.cards) == 4:
            self.hand = hand
        else:
            self.hand = Deck()
            
        self.board = None
        self.order = None
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def assign(self):
        while True:
            print("Deck: " + str(self.hand))
            x = h.get_int("select first positive card: ", sign = 1)
            y = h.get_int("select second positive card: ", sign = 1)
            
            if self.hand.check([x, y]):
                indices = self.hand.get_indices([x,y])
                
                dummy = Deck([])
                
                for i in range(4):
                    if i in indices:
                        dummy.cards.append(self.hand.cards[i])
                    else:
                        dummy.cards.append(-self.hand.cards[i])
                
                confirmation = input("Do you want to use " + str(dummy) + " as your deck? (y/n) \n")
                
                if confirmation == 'y' or confirmation == 'Y':
                    self.hand = dummy
                    break
                else:
                    print("Reassigning...\n")
                    continue
            
            print("You don't hold those cards.\n")
    
    def place(self):
        print("Available cards are: " + str(self.hand))
        while True:
            card = h.get_int("Select a card or enter 0 if you do not wish to play a card: ", sign = 1)
            if self.hand.check([card]):
                index = self.hand.get_indices([card])[0]
                self.hand.cards[index] = None
                return card
            
            elif card == 0:
                return card
            
            else:
                print("you are not holding that card")
    
    def stick(self):
        answer = input("Would you like to stick? (y/n)\n")
        if answer == "y" or answer == "Y":
            return True
        else:
            return False
    

class bot():
    def __init__(self, name = "C3-PO", hand = Deck()):
        if isinstance(name, str):
            self.name = name
        else:
            self.name = str(name)
        
        if isinstance(hand, Deck) and len(hand.cards) == 4:
            self.hand = hand
        else:
            self.hand = Deck()
        
        self.board = None
        self.order = None
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
    
    def assign(self):
        self.hand.cards[2] = -self.hand.cards[2]
        self.hand.cards[3] = -self.hand.cards[3]
        
    def place(self):
        
        card = 0
        if self.board.stick[1 - self.order]:
            target_range = range(self.board.round_score[1 - self.order], 21)
            
            if self.board.round_score[self.order] in target_range:
                card = 0
            else:
                candidates = set()
                for card in self.board.available_actions():
                    if (self.board.round_score[self.order] + card) in target_range:
                        candidates.add(card)
                
                if candidates:
                    card = max(candidates)
                    index = self.hand.get_indices([card])[0]
                    self.hand.cards[index] = None
                    
                else:
                    card = 0
        
        else:
            target_range = range(18, 21)
            
            if self.board.round_score[self.order] in target_range:
                card = 0
            else:
                candidates = set()
                for card in self.board.available_actions():
                    if (self.board.round_score[self.order] + card) in target_range:
                        candidates.add(card)
                
                if candidates:
                    card = max(candidates)
                    index = self.hand.get_indices([card])[0]
                    self.hand.cards[index] = None
                
                else:
                    card = 0
        
        if card:
            print(self.name + " plays a " + str(card))
        else:
            print(self.name + " does not play a card")
        
        return card
    
    def stick(self):
        if self.board.stick[1 - self.order]:
            target_range = range(self.board.round_score[1 - self.order], 21)
            
            if self.board.round_score[self.order] in target_range:
                print(self.name + "sticks.")
                return True
            
            else:
                return False
        
        else:
            target_range = range(18,21)
            
            if self.board.round_score[self.order] in target_range:
                return True
            
            else:
                return False


class pazaak():
    
    def __init__(self, player0 = None, player1 = None):
        
        if player0 == None:
            self.player0 = human()
        else:
            self.player0 = player0
        
        if player1 == None:
            self.player1 = human(name = "Han")
        else:
            self.player1 = player1
        
        self.players = [self.player0, self.player1]
        self.stick = [False, False]
        
        self.round_score = [0, 0]
        self.game_score = [0, 0]
        self.player = 0
        self.winner = None
    
    def __str__(self):
        x = "Rounds: " + str(self.game_score[0]) + " - " + str(self.game_score[1])
        y = "Score: " + str(self.round_score[0]) + " - " + str(self.round_score[1])
        return x + "\n" + y 
    
    def available_actions(self):
        actions = set()
        actions.add(0)
        
        for card in self.players[self.player].hand.cards:
            if card is not None:
                actions.add(card)
        
        return actions
    
    
    @classmethod
    def other_player(cls, player):
        if player:
            return 0
        else:
            return 1
            
    
    def opponent(self, player):
        if player == self.player0:
            return self.player1
        elif player == self.player1:
            return self.player0
        else:
            raise ValueError
    
    def switch_player(self):
        self.player = pazaak.other_player(self.player)
    
    """ Update game scores to reflect that a card has been placed."""
    def move(self, card):
        if self.winner is not None:
            raise Exception("Game has already been won")
        else:
            self.round_score[self.player] += card
            self.switch_player()
            
    """ Takes a player object as an input and updates the game state to reflect 
        that player's victory."""
    def round_win(self, player):
        self.game_score[player] += 1
        self.round_score = [0, 0]
        self.stick = [False, False]
        
        #Declare winner if a player has won their third round
        if self.game_score[player] == 3:
            self.winner = player
            print("The winner is " + str(self.players[player]))
            return player
            
        else:
            return None


def play(player0 = human(name = "Han"), player1 = human(name = "Greedo")):
    
    #create hands for each player
    hand0 = Deck(rolln(6, 1, 4))
    hand1 = Deck(rolln(6, 1, 4))
    
    player0.hand = hand0
    player0.order = 0
    
    player1.hand = hand1
    player1.order = 1
    
    #create new game
    game = pazaak(player0, player1)
    
    player0.board = game
    player1.board = game
    
    player0.assign()
    player1.assign()
    
    #game loop
    while True:
        #time.sleep(0.5)
        print("\n" + str(game) + "\n")
        
        print(str(game.players[game.player]) + " to move.")
        
        #draw new card
        print("Drawing card...\n")
        new_card = roll(10)
        time.sleep(0.75)
        
        #add new card to player score 
        game.round_score[game.player] += new_card
        print("Card: " + str(new_card) + "\nScore: " + str(game.round_score[game.player]))
                
        #remind player of their opponent's situation
        connective = " is on "
        if game.stick[1 - game.player]:
            connective = " has stuck on "
        
        print("Opponent" + connective + str(game.round_score[1 - game.player]))        

        
        #ask player for move
        placed_card = game.players[game.player].place()
        game.round_score[game.player] += placed_card
        
        #ask player to stick or twist
        game.stick[game.player] = game.players[game.player].stick()
        
        
        #check for bust
        if game.round_score[game.player] > 20:
            game.round_win(1 - game.player)
            if game.winner != None:
                break
            else:
                game.switch_player()
                continue


        #check for winner
        if all(game.stick):
            if game.round_score[0] > game.round_score[1]:
                game.round_win(0)
                game.switch_player()
                
                if game.winner != None:
                    break
                else:
                    continue
            
            elif game.round_score[1] > game.round_score[0]:
                game.round_win(1)
                game.switch_player()
                
                if game.winner != None:
                    break
                else:
                    continue
            
            else:
                game.round_score = [0, 0]
                game.stick = [False, False]
                game.switch_player()
                continue
                
        elif not game.stick[1 - game.player]:
            game.switch_player()
            continue
            
        else:
            continue
        
    del game
    del player0
    del player1
        
        
        
            

def test(test_player = human(name = "Han"), opponent = bot(name = "C3-PO"), round_score = None, game_score = None, opponent_stick = None, hand_initialize = True):
    
    #Initialize hands
    if hand_initialize == True:
        cards = []
        print("What cards is " + str(test_player) + " holding?\n")
        for i in range(4):
            card = h.get_int("Card " + str(i) + ":\n", sign = 1)
            if card:
                cards.append(card)
            else:
                cards.append(None)
        test_player.hand = Deck(cards)
    
        test_player.assign()
    
    else:
        print("Randomly generating a full hand...")
        test_hand = Deck(rolln(6, 1, 4))
        test_player.hand = test_hand
        test_player.assign()
    
    opponent_hand = Deck(rolln(6, 1, 4))
    opponent.hand = opponent_hand
    opponent.assign()
    
    
    test_player.order = 0
    opponent.order = 1
        
    
    #create new game
    game = pazaak(test_player, opponent)
    
    test_player.board = game
    opponent.board = game

    ###INITIALIZE GAME STATE
    #round score
    if round_score == None:
        round_score0 = h.get_int(str(test_player) + "'s round score:\n", sign = 1)
        round_score1 = h.get_int(str(opponent) + "'s round score:\n", sign = 1)
        game.round_score = [round_score0, round_score1]
        
    else:
        if not isinstance(round_score, list):
            raise ValueError
        elif len(round_score) != 2:
            raise ValueError
        else:
            game.round_score = round_score
    
    #game score
    if game_score == None:
        game_score0 = h.get_int(str(test_player) + "'s game score:\n", sign = 1)
        game_score1 = h.get_int(str(opponent) + "'s game score:\n", sign = 1)
        game.game_score = [game_score0, game_score1]
    
    else:
        if not isinstance(game_score, list):
            raise ValueError
        elif len(game_score) != 2:
            raise ValueError
        else:
            game.game_score = game_score
    
    #opponent stick
    if not isinstance(opponent_stick, bool):
        game.stick[1] = h.get_bool("Has " + str(opponent) + " stuck?\n")
    else:
        game.stick[1] = opponent_stick
        
    
    #make a move
    connective = " is on "
    if game.stick[1]:
        connective = " has stuck on "
        
    print(str(opponent) + connective + str(game.round_score[1]))
    print(str(test_player) + " to play, on a score of " + str(game.round_score[0]))
    
    placed_card = game.players[game.player].place()
    game.round_score[game.player] += placed_card
    
