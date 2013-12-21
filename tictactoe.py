from random import randint
import sys

board = [
        [' ',' ',' '],
        [' ',' ',' '],
        [' ',' ',' ']
        ]

def draw_box_sample():
    box_sample = '''
|---|---|---|
|   |   |   |
|---|---|---|
|   |   |   |
|---|---|---|
|   |   |   |
|---|---|---|
'''
    return box_sample

def user_coin(user='c'):
    return 'x' if user == 'h' else 'o'

def empty_slots():
    return [17, 21, 25, 45, 49, 53, 73, 77, 81]

def offsets():
    return [16, 19, 22, 41, 44, 47, 66, 69, 72]

def draw_board():
    global board
    box_sample_list = [c for c in draw_box_sample()]

    for x in range(0,3):
        for y in range(0, 3):
            pos = (x*3) + (y+1)
            offset = offsets()[pos-1]
            pos = offset + pos
            box_sample_list[pos] = board[x][y]

    return ''.join(box_sample_list)

def is_board_empty():
    l = [ elem for row in board for elem in row if elem.strip() > '' ]
    return False if l else True

def is_legal_move(pos):
    x, y = (pos-1)/3, (pos-1) % 3
    return True if (board[x][y].strip() == '') else False

def make_move(user='c', pos=0, name=''):
    global board
    x, y = (pos-1)/3, (pos-1) % 3

    # Check if board is already occupied at the position
    if not is_legal_move(pos):
        return 'Hey {}, Illegal move!\n'.format(name) + draw_board()

    # Make move
    coin = user_coin(user)
    board[x][y] = coin

    return draw_board()

def get_winning_positions():
    return [
            [1,2,3], 
            [4,5,6], 
            [7,8,9], 
            [1,4,7],
            [2,5,8],
            [3,6,9],
            [1,5,9],
            [3,5,7]
            ]

def get_winning_positions_sets():
    return [ set(x) for x in get_winning_positions() ]

def declare_win(user):
    h_win = 'You win! I lose. :('
    c_win = 'I win! You lose. :)'
    return h_win if user == 'h' else c_win

def check_win(user):
    winning_positions_sets = get_winning_positions_sets()
    coin = user_coin(user)
    user_position_set = set([ i+1 for i, x in enumerate([elem for row in board for elem in row ]) if x.strip() > '' and x == coin ])
    win_set = [ pos for pos in winning_positions_sets if (user_position_set & pos) == pos ]
    return True if win_set else False

def human_make_move(pos=0, name=''):
    return make_move('h', pos, name)

def computer_make_move():
    # Choose a random position based on chance of winning
    # If this is the first move, just start in some random position
    # If this is a subsequent move, check the earlier position of computer
    # and align to that optimally.
    if is_board_empty():
        pos = randint(1, 9)
        return make_move('c', pos)

    human_coin = user_coin('h')
    computer_coin = user_coin('c')

    human_moves = []
    computer_moves = []

    b = [elem for row in board for elem in row]
    for elem in b:
        human_moves = set([ i+1 for i, x in enumerate(b) if x.strip() == human_coin ])
        computer_moves = set([ i+1 for i, y in enumerate(b) if y.strip() == computer_coin ])
        empty_spaces = set([ i+1 for i, z in enumerate(b) if z.strip() == '' ])

    winning_positions_sets = get_winning_positions_sets()
    for w in winning_positions_sets:
        h_avail = w - human_moves
        if len(h_avail) == 1:
            p = h_avail.pop()
            if is_legal_move(p):
                return make_move('c', p) 

    for w in winning_positions_sets:
        h_avail = w - human_moves

        # If moves available to humans are same as the current winning set,
        # chances are that human might have made a move in another set
        # so, continue checking
        if (h_avail) == w:
            #print 'Continuing...'
            continue

        # If human has steps available, thwart it by taking the 
        # immediately available pos after this
        if len(h_avail) > 0:
            p = h_avail.pop()
            if is_legal_move(p):
                return make_move('c', p) 


print draw_board()
human_name = raw_input('Hey dude, what\'s your name? ')
move_prompt = 'Your move, {}?: '.format(human_name)
pos = int(raw_input(move_prompt))

while int(pos) != -1:
    print human_make_move(pos=pos, name=human_name)
    if check_win('h'):
        print declare_win('h')
        sys.exit()
    
    print 'My move: '
    print computer_make_move()
    if check_win('c'):
        print declare_win('c')
        sys.exit()

    pos = int(raw_input(move_prompt))

