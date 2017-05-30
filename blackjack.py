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

    def add_card(self, card):
        self.hand.append(card)

    # Returns a list of potential values based on current hand of cards.
    # If the return is an empty list, than the hand is bust. (Over 21, always)
    def potential_values(self):
        # Count how many aces there are. Summate value of non ace cards
        count_aces = 0
        base_val = 0
        for card in self.hand:
            if card.rank == "Ace":
                count_aces += 1
            elif card.rank in self.ranks[1:]:
                base_val += self.values[self.ranks.index(card.rank)]

        # Though rare, it could be possible to draw all 4 aces without bust
        # 1 Ace: [1, 11]
        # 2 Ace: [2, 12, 22, ...]
        # 3 Ace: [3, 13, 23, ...]
        # 4 Ace: [4, 14, 24, ...]
        # Since greater than 21 is automatic bust, only the first two values
        # in all cases needs to be included. Conviently it increments by 1
        # with number of aces.
        if count_aces == 0:
            values = [base_val]
        elif count_aces > 0 and count_aces < 5:
            possible_ace = [1 + count_aces - 1, 11 + count_aces - 1]
            values = [base_val + possible_ace[0], base_val + possible_ace[1]]
        else:
            print("ERROR")

        # Remove any values greater than 21
        values = [value for value in values if value <= 21]
        return values

    def bust(self):
        return len(self.potential_values()) == 0

    def clear(self):
        self.hand = []

    def print_hand(self):
        if len(self.hand) == 0:
            print(self.name, "- Hand Empty")
        else:
            print(self.name, "- Possible Value: ", self.potential_values())
            for card in self.hand:
                print(card)


# Dealer is responsible for dealing cards and deciding winners
class BlackJackDealer(Deck):
    # Dealer will hit if minimum hand value below 17.
    hit_target = 17

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
            self.dealer_hand.clear()
            self.player_hand.clear()

    def round_start(self):
        # Dealer & player starts with two cards
        self.dealer_hand.add_card(self.draw_card())
        self.dealer_hand.add_card(self.draw_card())
        print("Dealer visible card: ", self.dealer_hand.hand[0])
        self.player_hand.add_card(self.draw_card())
        self.player_hand.add_card(self.draw_card())
        self.player_hand.print_hand()
        # Does player want to hit?
        choice = None
        while(not self.player_hand.bust() and choice != "S"):
            choice = input("Choose to: (Q)uit, (H)it, (S)tand - ")
            if choice == "Q":
                print("Ending game...")
                return "Q"
            elif choice == "H":
                self.player_hand.add_card(self.draw_card())
                self.player_hand.print_hand()
            elif choice == "S":
                # Auto choose the max possible value
                player_hand_value = max(self.player_hand.potential_values())
                print("Stand - Using Value:", player_hand_value)

        # Dealer will stand on soft 18, hard 17 or higher.
        # Stop accepting cards if above happens, or the hand goes bust
        while(True):
            if max(self.dealer_hand.potential_values()) >= self.hit_target + 1:
                break  # Soft 18 or higher - do not take cards
            elif min(self.dealer_hand.potential_values()) == self.hit_target:
                break  # Hard 17 - do not take cards
            else:
                self.dealer_hand.add_card(self.draw_card())
            if self.dealer_hand.bust():
                break

        # Select best value for dealer hand
        if not self.dealer_hand.bust():
            dealer_hand_value = max(self.dealer_hand.potential_values())
        # Who wins?
        winner = None

        if self.player_hand.bust():
            print("Player Hand Bust! Dealer Wins! Starting next round...")
            winner = "dealer"
        elif self.dealer_hand.bust():
            print("Dealer Hand Bust! Player Wins! Starting next round...")
            winner = "player"
        elif dealer_hand_value > player_hand_value:
            print("Dealer wins with", dealer_hand_value)
            winner = "dealer"
        elif dealer_hand_value < player_hand_value:
            print("Player wins against", dealer_hand_value)
            winner = "player"
        elif dealer_hand_value == player_hand_value:
            print("Player ties against", dealer_hand_value)
            winner = "tie"
        else:
            print("Unexpected Case")
        print('**************')
        self.dealer_hand.print_hand()
        print('**************')
        return winner


new_game = BlackJackDealer()
new_game.game_start()
