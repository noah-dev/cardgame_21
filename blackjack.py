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
        return self.rank + " " + self.color + " " + self.suit


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
        card = self.deck.pop(0)
        self.used_cards.append(card)
        return card

    def print_cards(self):
        for card in self.deck:
            print(card)


class BlackJackGame(Deck):

    values = [999, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def hit(self):
        card = self.draw_card()
        if card.rank == "Ace":
            ace_choice = input('Ace drawn - 1 or 11?')
        else:
            ace_choice = "N/A"
        value = self.rank_to_value(card, ace_choice)
        return card, value

    def rank_to_value(self, card, ace_choice):
        inst_values = self.values
        # Does the player choose ace to be 1 or 11?
        if ace_choice == "1":
            inst_values[0] = 1
        elif ace_choice == "11":
            inst_values[0] = 11

        val_index = self.ranks.index(card.rank)
        return inst_values[val_index]


new_deck = Deck()
print(new_deck.draw_card())
print(len(new_deck.deck))
print(new_deck.used_cards[0])
print("----")
new_game = BlackJackGame()
card, value = new_game.hit()
print(card, value)
