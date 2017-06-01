"""Provides code to start a simplified version of 21/Blackjack.
    Example:
        import card_21
        game_inst = card_21.Dealer()
        game_inst.game_start()
"""
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

# Used by Deck for shuffle cards
import random


class CONSTANTS:
    """Class that holds constant used for card_21 file, such as card
    ranks (e.g. "Ace", "2", etc...), cards suits ("Clubs", "Diamond", etc...)
    or the target value the dealer will aim for.
    """
    RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King"]
    SUITS = {'clubs': {'name': "Clubs", 'color': "Black"},
             'diamond': {'name': "Diamond", 'color': "Red"},
             'hearts': {'name': "Hearts", 'color': "Black"},
             'spades': {'name': "Spades", 'color': "Red"}}
    VALUES = [999, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    # The dealer will aim for a hand value of 17 or higher.
    # Different behavior if hand value is a soft 17 (an Ace in the hand)
    DEALER_TARGET = 17


class Card:
    """Digital representaton of a card."""

    def __init__(self, rank, suit, color):
        """This class has 4 attributes - 3 set here, the 4th as a @property

        Args:
            rank (str): What rank is this card? (e.g. "King" )
            suit (str): What suit is this card? (e.g. "Diamond" )
            color (str): What color is this card? (e.g. "Red" )

        Attributes:
            rank (str): Set by rank argument
            suit (str): Set by suit argument
            color (str): Set by color argument
            attributes (list): @property - rank, suit and color in a list
        """
        self.rank = rank
        self.suit = suit
        self.color = color

    @property
    def attributes(self):
        """Return rank, suit, and color in a list"""
        return [self.rank, self.suit, self.color]

    @attributes.setter
    def attributes(self, attributes):
        """Set rank, suit and color with a list

        Args:
        attributes (list): A list of three strings for rank, suit and color
        """
        self.rank, self.suit, self.color = attributes

    def __repr__(self):
        template = str.join("", (self.__class__.__name__,
                                 "('{}', '{}', '{}')"))
        return template.format(*self.attributes)

    def __str__(self):
        template = "Rank: {0:5} | Suit: {1:7} | Color: {2}"
        return template.format(*self.attributes)

    def __eq__(self, other):
        """Compare two Card Objects. Do they have identical attributes?

        Args:
        other (Card): Another cared to compare too

        Returns:
        bool:   True if card's attribute is equal to other card's attribute
                False otherwise
        """
        return self.attributes == other.attributes

    def __ne__(self, other):
        """Compare two Card Objects. Do they have different attributes?
        Args:
        other (Card): Another cared to compare too

        Returns:
        bool:   True if card's attribute is not equal to other card's attribute
                False otherwise. (It's a  of __eq__)
        """
        return not self.__eq__(other)


class Deck:
    """Digital represention of a single deck of 52 cards"""
    RANKS = CONSTANTS.RANKS
    SUITS = CONSTANTS.SUITS

    def __init__(self, shuffle=True):
        """Creates a deck of cards.

        Args:
            shuffle (bool): Should the deck be initially shuffled / unshuffled?

        Attributes:
            deck (list): instance's deck, holding a list of cards
            deck_size (int): @property - how many cards in deck?
            empty (bool): @property - is the deck empty?
            is_shuffled (bool): @property - is the deck shuffled?
        """
        self.deck = []
        self.remake(shuffle=shuffle)

    def __repr__(self):
        template = str.join("", (self.__class__.__name__, "({})"))
        return template.format(self.is_shuffled)

    def __str__(self):
        template = "Deck has {} cards. Is shuffled? {}"
        return template.format(self.deck_size, self.is_shuffled)

    def remake(self, shuffle=True):
        """Create a new deck and assign to instance's deck


        """
        self.deck = self._make_deck(shuffle=shuffle)

    def _make_deck(self, shuffle=True):
        """Create a deck of cards. Used either for assignment or comparison


        """
        def make_suit(ranks, color, suit):
            return [Card(rank, color, suit) for rank in ranks]
        # For each suit, build its set of cards with make_suit
        deck_by_suit = [make_suit(self.RANKS,
                                  self.SUITS[suit]['name'],
                                  self.SUITS[suit]['color'])
                        for suit in self.SUITS.keys()]
        # Flatten the list, no longer split by suit
        deck = [card for sublist in deck_by_suit for card in sublist]
        if shuffle:
            random.shuffle(deck)
        return deck

    @property
    def deck_size(self):
        """Number of cards in instance's deck

        """
        return len(self.deck)

    @property
    def empty(self):
        """Are there no cards in the instance's deck?

        """
        return self.deck_size == 0

    @property
    def is_shuffled(self):
        """Compare the deck with a freshly made, unshuffled deck"""
        # List comprehension compares instance's deck with the freshly made
        # unshuffled deck, returning a list of bools. If all cards match in
        # order, the result is a list full of True. All() reduces this to True
        return not all([card == compare_card for card, compare_card
                        in zip(self.deck, self._make_deck(shuffle=False))])

    def shuffle_deck(self):
        """Shuffle the instance's deck"""
        random.shuffle(self.deck)

    def draw_card(self):
        """Remove a card from the top of the deck and return it.

        Args:
        self (Deck):
        """
        if self.empty:
            return None
        else:
            return self.deck.pop(0)

    def print_cards(self):
        print("Printing deck (ID: {})".format(id(self)))
        [print(card) for card in self.deck]


# Digital equivalent of a hand of cards. Responsible for managing cards and
# figuring out valid values (e.g. an Ace card + 6 card can be 7 or 17)
class Hand():
    VALUES = CONSTANTS.VALUES
    RANKS = CONSTANTS.RANKS

    def __init__(self, owner_name):
        # Name of the hand's owner (e.g. "Dealer" or "Player")
        self.owner_name = owner_name
        # Holds the cards - hand is initially empty
        self.cards = []

    # Add a card object to the hand
    def add_card(self, card):
        self.cards.append(card)

    # Returns a list of potential values based on current hand of cards.
    # If the return is an empty list, than the hand is bust. (Over 21, always)
    @property
    def potential_values(self):
        # Count how many aces there are. Summate value of non ace cards
        count_aces = 0
        base_val = 0
        for card in self.cards:
            if card.rank == "Ace":
                count_aces += 1
            elif card.rank in self.RANKS[1:]:
                base_val += self.VALUES[self.RANKS.index(card.rank)]

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
        elif count_aces >= 1 and count_aces <= 4:
            possible_ace = [1 + count_aces - 1, 11 + count_aces - 1]
            values = [base_val + possible_ace[0], base_val + possible_ace[1]]
        else:
            raise Exception("Number of counted aces greater than 4")

        # Remove any values greater than 21
        values = [value for value in values if value <= 21]
        return values

    # Call to figure out if the hand is bust.
    # potential_values ignores hand values over 21.
    # So if the list is empty, the hand's value is over 21 (Bust)
    @property
    def bust(self):
        return len(self.potential_values) == 0

    @property
    def empty(self):
        return len(self.cards) == 0

    # Set the hand to an empty set, clearing the cards
    def clear(self):
        self.cards = []

    # Print out every card in the hand to stdin.
    def print_hand(self):
        name = self.owner_name
        if self.empty:
            print("Hand of", name, "- Hand Empty")
        else:
            if self.bust:
                print("Hand of", name, "- Hand is Bust ")
            else:
                print("Hand of", name, "- Possible Value: ",
                      self.potential_values)
            for card in self.cards:
                print(card)


# Dealer is responsible for dealing cards and deciding winners
class Dealer(Deck):

    def __init__(self):
        # Build and shuffle the deck
        super(Dealer, self).__init__()
        # Initalize dealers hand and deal two cards
        self.dealer_hand = Hand("Dealer")
        self.player_hand = Hand("Player")
        self.TARGET = CONSTANTS.DEALER_TARGET

    def game_start(self):
        quit = False
        while(not quit):
            print("--------------------")
            result = self.round_start()
            if result == "Q":
                quit = True

            # Clear the hand after a round is complete
            self.dealer_hand.clear()
            self.player_hand.clear()

            # Rebuild and reshuffle deck after each round
            self.remake(shuffle=True)
            # If the game is over, do not prompt for next round
            if not quit:
                input("Press enter for next round...")

    def round_start(self):
        # Dealer & player starts with two cards
        self.dealer_hand.add_card(self.draw_card())
        self.dealer_hand.add_card(self.draw_card())
        self.player_hand.add_card(self.draw_card())
        self.player_hand.add_card(self.draw_card())

        # Show dealer's face up card and player's hand
        print("Dealer visible card: ", self.dealer_hand.cards[0])
        self.player_hand.print_hand()

        # Check for natrual (ace + 10 value card)
        natural = False
        natural, winner = self.check_natural(self.player_hand,
                                             self.dealer_hand)
        if natural:
            if winner == "Dealer":
                print("Dealer's first two cards are natural - Dealer Wins!")
            elif winner == "Tie":
                print("Both Dealer's and Player's first two cards",
                      "are natural - Tie!")

            print('**************')
            self.dealer_hand.print_hand()
            print('**************')
            return winner

        # Does player want to hit?
        choice = None
        while(not self.player_hand.bust and choice != "S"):
            choice = input("Choose to: (Q)uit, (H)it, (S)tand - ")
            if choice == "Q":
                print("Ending game...")
                return "Q"
            elif choice == "H":
                self.player_hand.add_card(self.draw_card())
                self.player_hand.print_hand()
            elif choice == "S":
                # Auto choose the max possible value
                player_hand_value = max(self.player_hand.potential_values)
                print("Stand - Using Value:", player_hand_value)

        # Dealer stand for hand value of 17 - will hit on soft 17
        while(not self.player_hand.bust):
            if max(self.dealer_hand.potential_values) >= self.TARGET + 1:
                break  # Soft 18 or higher - do not take a card
            elif min(self.dealer_hand.potential_values) == self.TARGET:
                break  # Hard 17 - do not take a card
            else:
                # Either less than 17 or a soft 17 - take a card
                self.dealer_hand.add_card(self.draw_card())
            # If the dealer's hand is bust, break
            if self.dealer_hand.bust:
                break
        # Who wins?
        return self.pick_winner(self.player_hand, self.dealer_hand)

    # If dealer draws an ace and a 10 value card, the round ends immediatly
    # If the player also has an ace and a 10 value card, a tie is declared.
    # Otherwise the dealer wins.
    def check_natural(self, player_hand, dealer_hand):
        if max(dealer_hand.potential_values) == 21:
            if max(player_hand.potential_values) == 21:
                return True, "Tie"
            else:
                return True, "Dealer"
        else:
            return False, "N/A"

    def pick_winner(self, player_hand, dealer_hand):
        # Select best value for player and dealer
        if not self.player_hand.bust:
            player_hand_value = max(self.player_hand.potential_values)

        if not self.dealer_hand.bust:
            dealer_hand_value = max(self.dealer_hand.potential_values)

        winner = None

        if self.player_hand.bust:
            print("Player Hand Bust! Dealer Wins! Starting next round...")
            winner = "dealer"
        elif self.dealer_hand.bust:
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
