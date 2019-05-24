# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
loser = False
outcome = ""
query = ""
score = 5 # $250
loaned = 0
MAX_LOAN = 1000
BET_SIZE = 50

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self): # create Hand object
        self.cards = []

    def __str__(self): # return a string representation of a hand
        s = "hand contains "
        for card in self.cards:
            s = s + str(card) + " "
        return s

    def add_card(self, card): # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        val = 0
        ace = False
        for card in self.cards:
            val += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace = True
        if ace and val <= 11:
            val += 10
        return val
   
    def draw(self, canvas, pos): # draw a hand on the canvas, use the draw method for cards
        i = 0
        while i < len(self.cards):
            self.cards[i].draw(canvas, [pos[0] + i * CARD_SIZE[0], pos[1]])
            i += 1
 
# define deck class 
class Deck:
    def __init__(self): # create a Deck object
        self.deck = []
        #deck = [Card(s, r) for s in suits [for r in ranks]]
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self): # deal a card object from the deck
        return self.deck.pop(random.randrange(len(self.deck)))
    
    def __str__(self): # return a string representing the deck
        s = "Deck contains "
        for card in self.deck:
            s = s + str(card) + " "
        return s

def broke():
    global outcome, query, loser, in_play
    in_play = False
    if loaned >= MAX_LOAN:
        loser = True
    else:
        outcome = "You're out of money."
        query = "Take a loan?"
    
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, query
    if loser:
        return
    if score <= 0:
        broke()
        return
    
    if in_play:
        outcome = "You lose this round."
        score -= 1
        if score <= 0:
            broke()
            return
    else:
        outcome = ""
        
    deck = Deck()
    deck.shuffle()
    dealer_hand, player_hand = Hand(), Hand()
    
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_s = str(dealer_hand)
    
    print # console output, hiding first dealer card
    print "Dealer " + dealer_s[0:14] + "XX" + dealer_s[16:]
    print "Player " + str(player_hand)
    
    in_play = True
    query = "Hit or stand?"

def hit():
    global outcome, in_play, score, query
    if loser:
        return    
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        print "Player " + str(player_hand)
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You have busted!"
            score -= 1
            in_play = False
            query = "New deal?"
            print outcome
            print "New score:", score
    else:
        outcome = "This game is over."
       
def stand():
    global in_play, outcome, score, query
    if loser:
        return
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        print "Dealer " + str(dealer_hand)
        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = "Dealer have busted, you win!"
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer wins!"
            score -= 1
        else: # player wins
            outcome = "Player wins!"
            score += 1
        in_play = False
        query = "New deal?"
        print "Player = " + str(player_hand.get_value()) + "; Dealer = " + str(dealer_hand.get_value())
        print outcome
        print "New score:", score
    else:
        outcome = "This game is over."

def loan():
    global loaned, score, query, outcome, loser
    if loser:
        return
    if loaned < MAX_LOAN:
        score += (MAX_LOAN / BET_SIZE) / 10 # 2
        loaned += MAX_LOAN / 10 # 100
    else:
        outcome = "You can't loan any more."
        if score <= 0: # also out of money
            loser = True
    
# draw handler    
def draw(canvas):
    if loser:
        canvas.draw_text("You lost everything.", [100, 280], 50, "Black", "sans-serif")
        canvas.draw_text("Better luck next time...", [150, 350], 35, "Black", "serif")
        return
    # game title
    canvas.draw_text("Blackjack", [400, 60], 40, "Black", "sans-serif")
    # dealer hand
    canvas.draw_text("Dealer", [20, 90], 30, "Black", "serif")
    dealer_hand.draw(canvas, [20, 100])
    if in_play: # cover first card
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [20 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)
    # player hand
    canvas.draw_text("Player", [20, 390], 30, "Black", "serif")
    player_hand.draw(canvas, [20, 400])
    # outcome and query
    canvas.draw_text(outcome, [20, 270], 35, "Black", "serif")
    canvas.draw_text(query, [20, 320], 35, "Black", "serif")
    # score
    canvas.draw_text("Money: $" + str(score * BET_SIZE), [250, 550], 30, "Black", "serif")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Take a loan for $100", loan, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric