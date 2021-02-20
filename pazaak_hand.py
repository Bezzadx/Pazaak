from dice import *


class hand():
    def __init__(self, cards):
        self.cards = cards
        
    def __str__(self):
        return str(self.cards)
    
    def __repr__(self):
        return str(self.cards)
    
    
    def check(self, check_cards = []):
        for card in self.cards:
            for index, target in enumerate(check_cards):
                if card == target:
                    check_cards[index] = None
                    break
        
        return all(card == None for card in check_cards)
    
    def get_indices(self, get_cards = []):
        indices = [None for card in get_cards]
        
        for i, card in enumerate(self.cards):
            for j, target in enumerate(get_cards):
                if card == target:
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
    
    def remove(self, card):
        if card not in self.cards:
            return 0
        else:
            index = self.get_indices([card])[0]
            return self.cards.pop(index)