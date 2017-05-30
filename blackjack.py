from random import shuffle


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
    hand = []
    hand_total = 0
    ranks = []
    values = []

    def __init__(self, ranks, values):
        self.ranks = ranks
        self.values = values

    def add_card(self, card):
        self.hand.append(card)
        self.hand_total += self.rank_to_val(card)

    def clear_hand(self):
        self.hand = []
        self.hand_total = 0

    def print_hand(self):
        if len(self.hand) == 0:
            print("Hand Empty")
        else:
            print("Hand Value: ", self.hand_total)
            for card in self.hand:
                print(card)

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

    def __init__(self, ranks, values):
        self.hand = BlackJackHand(ranks, values)
        super(BlackJackDealer, self).__init__()

    def hit(self):
        return self.draw_card()


class BlackJackGame():
    values = [999, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King"]
    dealer = BlackJackDealer(ranks, values)
    hand1 = BlackJackHand(ranks, values)


new_game = BlackJackGame()
print("Welcome! Starting Game...")
again = "y"
while(again == "y"):
    card = new_game.dealer.hit()
    BlackJackGame.hand1.add_card(card)
    BlackJackGame.hand1.print_hand()
    if BlackJackGame.hand1.hand_total > 21:
        print("Went over 21! Bust! - Clearing Hand")
        BlackJackGame.hand1.clear_hand()
        print("Next Round...")
    again = input("Draw Again? y/n ")
    print("-----------")
