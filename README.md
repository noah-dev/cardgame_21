
# cardgame_21
This is one of my older side projects. I wanted to practice my OOP skills and figured a card-game would make for good practice. 
* Why? Though I was understood in OOP in principle, I wanted to put my understanding & skills to the test.
* How? Take a card and imagine each entity as an object. Each card is an object, with rank & suit. Each deck is an object made of 52 card objects. Each hand is made of several card objects that pull from the deck object. 
* What? Though the final result is nothing spectacular, it was a great learning experience. I become more confident with OOP in python and I learned new syntax and functions. Also, pointers finally make sense to me (not just in theory). 

# Game Rules
There is the player and the dealer. The dealer pulls cards from a shuffled deck for the player's hand and the dealer's hand. Each card has a value. The objective is to attain a hand with a cumulative value as close to 21, without going over; whoever is closer wins the round. Both player and dealer initially start with two cards and may pull more cards for their hands. 

**How is win/lose determined?**
* If the hand's cumulative value goes over 21, the hand's owner loses automatically. 
* If neither hand's cumulative value goes over 21, the hand which is higher in value wins.
* If the dealer achieves a cumulative value of 21 with the first two cards, the dealer wins outright.
* If the dealer's first two cards to not have a cumulative value of 21 and the player achieves a hand with a cumulative value of 21, the player wins. 

**Card Values:**
* Cards 1 through 10 are worth their numeric values. (e.g. a hand with a 3 of Spades and a 10 of Clubs is worth 13)
* Face cards are worth 10. (e.g. a hand with a 5 of Diamond and a King of Spades is worth 15)
* If an Ace is drawn, it can either be worth 1 or 11. (e.g. if the player has hand with Ace of Hearts and a 7 of Diamond, the hand is either worth 8 or 18)


# How did I approach this?
Imagine an actual game. The dealer is responsible for the deck, shuffling it, and providing cards to itself and the player. Let's walk through a scenario:
* A new game starts and the Dealer gets a deck of cards, shuffles it, and gives a pair of cards to its own hand and the player's hand.
* Based on the player's hand's cumulative value, the player either asks for a new card or does not. Say the player asks for a card.
* The dealer will pull a card from the top of the deck and give it to the player's hand. After one card, the player now stays.
* Based on the dealer's hand's cumulative value, the dealer may automatically draw new cards. Say the dealer draws one card.
* The dealer will pull a card from the top of the deck and give it to the dealer's hand. 
* Both player & dealer will reveal their hands. The dealer will declare the winner based on the results. 


**There is the dealer, which is a Dealer Class. Dealer class is responsible for:**
* Giving cards to the player's hand and managing it's own hand. Both player & dealer hand are objects of the **Hand class**.
* Managing the deck of cards, which is a **Deck class**. 
* Overseeing the game and declaring winner/loser. 

**There is the dealer's hand and the player's hand, which are both Hand class. Hand class is responsible for:**
* Holding any cards given to it. A card is an object of the **Card class**.
* Calculating the cumulative value of the hand.
* Determining if the hand is bust. 
* Removing all cards in the hand. 
* Printing out the hand's cards

**There is the deck, which is a Deck class. Deck class is responsible for:**
* Holding the remaining cards in the deck. A card is an object of the **Card class**. 
* Building a full set with 52 cards
* Shuffling the deck
* Providing a card from the top of the deck. 

**There is the card, which is a Card class. Card class is responsible for:**
* Holding the attributes of the card. (Rank & Suit)
* Determining if it equal to another card. (Same Rank & Same Suit)

![diagram.png](diagram.png)
