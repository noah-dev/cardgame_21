from random import shuffle
import os

# How classes are organized
# Game
# |--dealer
# |  |--hand (hand class)
# |  |--deck
# |     |--card
# |--player hand 1 (hand class)
# |--player hand 2 (hand class)
# |--etc...

# game is responsible for managing the transfer of cards between the deck
# and player hands.

# dealer is responsible for managing it's own hand and the deck

# hand class is responsible for managing a hand of cards for it's owner
# (owner being the dealer or a player)

# deck is a digital representation of a standard 52 card deck

# card is a digital representation of a single card


class Card:
    rank = ""
    color = ""
    suit = ""

    def __init__(self, rank, color, suit):
        self.rank = rank
        self.color = color
        self.suit = suit

    def __str__(self):
        return "Card: " + self.rank + ", " + self.color + ", " + self.suit


class Deck:
    deck = []
    used_cards = []
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King"]
    suits = ["Clubs, Diamonds, Hearts, Spades"]

    def __init__(self):
        # Build unshuffled_deck deck
        self.unshuffled_deck()
        # Shuffle deck
        self.shuffle_cards()
        self.shuffle_cards()
        self.shuffle_cards()

    def unshuffled_deck(self):
        def suit_maker(ranks, color, suit):
            suit_deck = []
            for rank in self.ranks:
                card = Card(rank, color, suit)
                suit_deck.append(card)
            return suit_deck

        # suits
        clubs = suit_maker(self.ranks, "Black", "Clubs")
        diamonds = suit_maker(self.ranks, "Red", "Diamonds")
        hearts = suit_maker(self.ranks, "Red", "Hearts")
        spades = suit_maker(self.ranks, "Black", "Spades")

        # combine the cards from all suits
        for suit in [clubs, diamonds, hearts, spades]:
            for card in suit:
                self.deck.append(card)

    def shuffle_cards(self):
        shuffle(self.deck)

    def draw_card(self):
        if len(self.deck) > 0:
            card = self.deck.pop(0)
            self.used_cards.append(card)
            return card
        else:
            return None

    def print_cards(self):
        for card in self.deck:
            print(card)


class BlackJackHand():
    values = [999, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King"]

    def __init__(self, name):
        self.name = name
        # Needed - otherwise both dealer and hand point to same thing
        self.hand = []

    def add_card(self, card, ace_choice):
        card_val = self.rank_to_val(card, ace_choice)
        self.hand.append({'card': card, 'card_value': card_val})

    @property
    def hand_value(self):
        hand_value = 0
        for card in self.hand:
            hand_value += card['card_value']
        return hand_value

    @property
    def hand_bust(self):
        return self.hand_value > 21

    def clear_hand(self):
        self.hand = []

    def print_hand(self):
        if len(self.hand) == 0:
            print(self.name, "- Hand Empty")
        else:
            print(self.name, "- Hand Value: ", self.hand_value)
            for card in self.hand:
                print(card['card'])

    def rank_to_val(self, card, ace_choice=0):
        inst_values = self.values

        if ace_choice == "1":
            inst_values[0] = 1
        elif ace_choice == "11":
            inst_values[0] = 11

        return inst_values[self.ranks.index(card.rank)]


# Dealer is responsible for dealing cards and deciding winners
class BlackJackDealer(Deck):
    def __init__(self):
        # Build and shuffle the deck
        super(BlackJackDealer, self).__init__()
        # Initalize dealers hand and deal two cards
        self.dealer_hand = BlackJackHand("Dealer")
        self.player_hand = BlackJackHand("Player")

    def game_start(self):
        quit = False
        while(not quit):
            print("--------------------")
            result = self.round_start()
            if result == "Q":
                quit = True
            self.dealer_hand.clear_hand()
            self.player_hand.clear_hand()

    def round_start(self):
        # Dealer & player starts with two cards
        self.dealer_decision()
        self.dealer_decision()
        print("Dealer visible card: ", self.dealer_hand.hand[0]['card'])
        print("Dealing player cards...")
        for i in range(2):
            self.deal_player()

        # Does player want to hit?
        choice = None
        while(not self.player_hand.hand_bust and choice != "S"):
            choice = input("Choose to: (Q)uit, (H)it, (S)tand - ")
            if choice == "Q":
                print("Ending game...")
                return "Q"
            elif choice == "H":
                self.deal_player()
            elif choice == "S":
                print("No Card Taken")
        # Does dealer want to hit?
        while(self.dealer_hand.hand_value < 18):
            self.dealer_decision()

        winner = None
        if self.player_hand.hand_bust:
            print("Player Hand Bust! Dealer Wins! Starting next round...")
            winner = "dealer"
        elif self.dealer_hand.hand_bust:
            print("Dealer Hand Bust! Player Wins! Starting next round...")
            winner = "player"
        elif self.dealer_hand.hand_value > self.player_hand.hand_value:
            print("Dealer wins with", self.dealer_hand.hand_value)
            winner = "dealer"
        elif self.dealer_hand.hand_value < self.player_hand.hand_value:
            print("Player wins against", self.dealer_hand.hand_value)
            winner = "player"
        elif self.dealer_hand.hand_value == self.player_hand.hand_value:
            print("Player ties against", self.dealer_hand.hand_value)
            winner = "tie"
        else:
            print("Unexpected Case")
        print('**************')
        self.dealer_hand.print_hand()
        print('**************')
        return winner

    def deal_player(self):
        card = self.draw_card()
        ace_choice = 0
        # If ace, player decides if 1 or 11
        if card.rank == "Ace":
            ace_choice = input("Ace Drawn - 1 or 11?")
        self.player_hand.add_card(card, ace_choice)
        self.player_hand.print_hand()

    # Does the dealer stay or hit?
    def dealer_decision(self):
        if self.dealer_hand.hand_value < 18:
            card = self.draw_card()
            self.dealer_hand.add_card(card, "11")
        else:
            pass


new_game = BlackJackDealer()
new_game.game_start()
