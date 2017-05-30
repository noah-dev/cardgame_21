from random import shuffle

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
    name = ""
    hand = []
    values = [999, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King"]

    def __init__(self, name):
        self.name = name
        # Needed - otherwise both dealer and hand point to same thing
        self.hand = []

    def __add__(self, card):
        card_val = self.rank_to_val(card)
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
            print("Hand Empty")
        else:
            print("Hand Value: ", self.hand_value)
            for card in self.hand:
                print(card['card'])

    def rank_to_val(self, card):
        inst_values = self.values

        # If the card is an ace, decide if it should be 1 or 11
        ace_choice = 0
        if card.rank == "Ace":
            while(ace_choice == 0):
                ace_choice = input("Ace Drawn - Choose 1 or 11: ")
                if ace_choice == "1":
                    inst_values[0] = 1
                elif ace_choice == "11":
                    inst_values[0] = 11
                else:
                    print("Choice not valid - please try again")
                    ace_choice = 0
        return inst_values[self.ranks.index(card.rank)]


# Dealer is responsible for both it's own hand and the deck
class BlackJackDealer(Deck):
    hand = []

    def __init__(self):
        # Build and shuffle the deck
        super(BlackJackDealer, self).__init__()
        # Initalize dealers hand and deal two cards
        self.hand = BlackJackHand("Dealer")
        self.new_hand()

    def new_hand(self):
        self.hand.clear_hand()
        self.hand + self.draw_card()
        self.hand + self.draw_card()

    def deal_dealer(self):
        if self.hand.hand_value < 17:
            card = self.draw_card()
            print("Dealer has hit...")
            self.hand + card
        else:
            print("Dealer has stayed...")


class BlackJackGame():
    dealer = BlackJackDealer()
    player = BlackJackHand("Player")

    def __init__(self):
        print("Welcome to blackjack! Starting game now...")
        self.start_game()

    def start_game(self):
        quit = False
        while(not quit):
            choice = None
            while choice is None:
                # Player decision
                choice = input("Choose to: (Q)uit, (H)it, (S)tand - ")
                if choice == "Q":
                    quit = True
                elif choice == "H":
                    self.deal_player(self.player)
                elif choice == "S":
                    print("No Card Taken - Current Hand Value:",
                          self.player.hand_value)
                else:
                    print("Choice not recognized - please try again")
                    choice = None

            # Check if player bust
            if self.player.hand_bust:
                self.player.print_hand()
                self.next_round()
                print("Bust! Player Loses. Starting next round...")
            # Let dealer decide if it wants to hit
            self.dealer.deal_dealer()
            # Check if bust
            if self.dealer.hand.hand_bust:
                self.dealer.hand.print_hand()
                self.next_round()
                print("Dealer Bust! Player Wins. Starting next round...")

            if self.compare() == "player":
                self.dealer.hand.print_hand()
                self.player.print_hand()
                self.next_round()
                print("Player Wins! Starting next round...")
            if choice == "S" and self.compare() == "dealer":
                self.dealer.hand.print_hand()
                self.player.print_hand()
                self.next_round()
                print("Dealer Wins! Starting next round...")

        print("Game Over")

    def next_round(self):
        self.player.clear_hand()
        self.dealer.hand.clear_hand()

    def deal_player(self, hand):
        card = self.dealer.draw_card()
        # BlackJackGame.hand1.add_card(card)
        hand + card
        hand.print_hand()

    def compare(self):
        print("Compare", self.dealer.hand.hand_value, self.player.hand_value)
        if self.dealer.hand.hand_value > self.player.hand_value:
            return "dealer"
        else:
            return "player"


new_game = BlackJackGame()
