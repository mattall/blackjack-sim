# blackjack-sim.py
# Written by Matt Nance Hall 
# April 4, 2021

from random import shuffle    
from time import sleep

card_values = { "ACE"   : 1,
                "KING"  : 10,
                "QUEEN" : 10,
                "JACK"  : 10, 
                "10"    : 10, 
                "9"     : 9, 
                "8"     : 8,
                "7"     : 7,
                "6"     : 6,
                "5"     : 5,
                "4"     : 4,
                "3"     : 3,
                "2"     : 2 }

class Card():
    def __init__(self, face:str, suit:str):
        self.face=face
        self.suit=suit

    def __repr__(self):
        return "{} of {}".format(self.face, self.suit)

    def __iter__(self):
        return iter((self.face, self.suit))

    def get_value(self):
        return card_values[self.face]


def init_deck():
    '''
    Creates a single deck of cards and returns it shuffled. 
    Cards are ordered tuples (FACE, SUIT)
    '''

    faces = ["ACE", "KING", "QUEEN", "JACK", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    suits = ["SPADES", "CLUBS", "DIAMONDS", "HEARTS"]

    deck = [Card(f, s) for f in faces for s in suits]
    play_print("Shuffling deck...")
    shuffle(deck)
    # print(deck)

    return deck 

def single_val(values):
    return max(values) if max(values) <= 21 else min(values)

def get_values(hand):
    values = [0, 0]
    for card in hand:
        face, suit = card
        if face == "ACE" and values[0] == values[1]:
            values[1] += 11
            values[0] += 1 
            
        else:
            values[0] += card_values[face]
            values[1] += card_values[face]

    return values


def show_value_of_cards(hand):
    values = get_values(hand)

    play_print("hand:", hand)
    if values[0] != values [1] and max(values) <= 21:
        play_print("value:", values[0], "OR", values[1])
    else: play_print("value:", values[0])

def play_print(*strings):
    for s in strings:
        print(s, end=' ')
    print("\n")
    sleep(2)

def play():
    dealer_hand = []
    play_print("Dealer draws a card face up.")
    dealer_hand.append(deck.pop())
    
    show_value_of_cards(dealer_hand)
    
    play_print("Dealer draws a card face down.")
    dealer_hand.append(deck.pop())

    play_print("Player draws two cards.")
    player_hand = []
    player_hand.append(deck.pop())
    player_hand.append(deck.pop())

    # player_hand = [Card('QUEEN', 'DIAMONDS'), Card('JACK', 'HEARTS')]
    
    show_value_of_cards(player_hand)

    hands = player_options(player_hand)
    dealer_val = single_val(get_values(dealer_hand))
    
    play_print('Dealer has: ', dealer_val)
    print("Player hands", hands)
    for hand in hands:
        play_print('Player has: ', single_val(get_values(hand)))

    dealer_hand = dealer_play(dealer_hand)

    for hand in hands:
        if single_val(get_values(hand)) <= 21 and single_val(get_values(dealer_hand)) > 21:
            play_print('Player with', hand, "Wins!!!")
        
        elif single_val(get_values(hand)) > 21:
            play_print('Player with', hand, "Loses :( Sorry!")

        elif single_val(get_values(hand)) <= 21 and single_val(get_values(dealer_hand)) <= 21:
            if single_val(get_values(hand)) == single_val(get_values(dealer_hand)):
                play_print('Player with', hand, "Pushes.")
            
            elif single_val(get_values(hand)) < single_val(get_values(dealer_hand)):
                play_print('Player with', hand, "Loses :( Sorry!")
            
            elif single_val(get_values(hand)) > single_val(get_values(dealer_hand)):
                play_print('Player with', hand, "Wins!!!")

        else:
            play_print("This is awkward...")


def player_options(hand, can_double_or_split=True):

    vals = get_values(hand)
    
    # Blackjack? 
    if 21 in vals:
        play_print("Blackjack!")
        return [hand]

    # Bust? 
    if vals[0] > 21 and vals[1] > 21:
        play_print("Bust :(")
        return [hand]

    while 1:
        option = input("What would you like to do? [Type Split, Double, Hit, or Stay. Then press enter.]\n> ").lower().strip()
        if option.lower() == "split":
            if hand[0].get_value() == hand[1].get_value():
                break
        
            play_print("Sorry, cannot split this hand!")
            print("Cards are:", hand[0], "and", hand[1])
            print("Values are:", hand[0].get_value(), "and", hand[1].get_value())

        elif option.lower() == "double":
            break
    
            play_print("Sorry, cannot double now.")

        elif option.lower() == "hit":
            break

        elif option.lower() == "stay":
            break

        else:
            play_print("Invalid selection.")

    # SPLIT
    if option == "split":
        play_print("Player splits their hand.")
        hands = [[hand.pop()], [hand.pop()]]
        
        new_hands = []
        for i in range(len((hands))):
            h = hands[i]
            h.append(deck.pop())
            show_value_of_cards(h)

            # store the hand that we played, and the new hand that results from 
            # plyer_options in the new_hands list as tuple (hand, new_hand)
            nested_hands = player_options(h)
            for nh in nested_hands:
                new_hands.append(nh)
   
        play_print(new_hands)
        return new_hands

    # DOUBLE? 
    elif option == "double":
        play_print("Player doubles down.")

        hit_card = deck.pop()   
        
        play_print(hit_card)
        
        hand.append(hit_card)
        
        show_value_of_cards(hand)
        
        return [hand]
    
    # HIT?
    elif option == "hit":
        play_print("Player hits and pulls a card: ")
        
        hit_card = deck.pop()   
        
        play_print(hit_card)
        
        hand.append(hit_card)
        
        show_value_of_cards(hand)

        hands = player_options(hand, can_double_or_split=False)
        return hands

    # STAY? 
    elif option == "stay":
        return [hand]


def dealer_play(dealer_hand):
    while single_val(get_values(dealer_hand)) < 17:
        
        card = deck.pop()
        play_print("dealer draws a card:", card)
        dealer_hand.append(card)
        show_value_of_cards(dealer_hand)
    
    if single_val(get_values(dealer_hand)) > 21:
        play_print("Dealer Busts!")
    
    return dealer_hand

deck = init_deck()
play()