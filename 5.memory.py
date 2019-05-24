# implementation of card game - Memory

import simplegui
import random

# initializing global constants
WIDTH = 800
HEIGHT = 100
CARD_WIDTH = 50
CARD_HEIGHT = 100
FONT_SIZE = 90

# helper function to initialize globals
def new_game():
    global deck, exposed, state, old_idx, turns
    state, turns = 0, 0
    label.set_text("Turns = 0")
    old_idx = []
    # initializing deck
    deck = range(0, 8) + range(0, 8)
    random.shuffle(deck)
    # initializing exposed list, all hidden by default
    exposed = [False for e in range(len(deck))]

# define event handlers
def mouseclick(pos):
    global exposed, state, old_idx, turns
    # -1 to -16 from right to left
    idx = -(1 + (WIDTH - pos[0] - 1) // CARD_WIDTH)
    
    # ignore clicks on open cards
    if exposed[idx]:
        return
    
    # 2 new cards were opened
    if state == 2:
        state = 1
        for o in old_idx:
            exposed[o] = False
        old_idx = [idx]
    # 1 new card was opened
    elif state == 1:
        turns += 1
        label.set_text("Turns = " + str(turns))
        if deck[idx] == deck[old_idx[0]]:
            # cards match
            old_idx = []
            state = 0
        else:
            old_idx.append(idx)
            state = 2
    # no new cards were opened
    else:
        state = 1
        old_idx.append(idx)
    exposed[idx] = True

def draw(canvas):
    # drawing numbers
    i = 0
    for card in deck:
        x = i * 50
        canvas.draw_text(str(card), [x, FONT_SIZE - 11],
                         FONT_SIZE, "White", "monospace")
        # drawing cards to cover numbers if they're not exposed
        if not exposed[i]:
            canvas.draw_polygon([[x, 0], [x + CARD_WIDTH, 0],
                                 [x + CARD_WIDTH, CARD_HEIGHT], [x, CARD_HEIGHT]],
                                1, "Black", "Green")
        i += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
