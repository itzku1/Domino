import re

# Constant strings of repeated prints to the user.
CHOOSE_ACTION = "Choose action: Tile (t) or Draw (d): "
ILLEGAL_MOVE = "Error: Illegal move"

# This class represents Tiles of a domino game.
# Each tile hold left and right values and can be rotated.
class Tile:
    # Constructor. Initialized with left and right values to create tile.
    def __init__(self, l, r):
        self.left = l
        self.right = r

    # Get right value of the tile.
    def get_right(self):
        return self.right

    # Get left value of the tile.
    def get_left(self):
        return self.left

    # Rotate the tile.
    def rotate(self):
        return Tile(self.right, self.left)

    # Calculates the score of a tile. This is necessary to determine how is the first player in a game.
    def score(self):
        if self.right == self.left:
            if self.left == 6:
                return 18
            elif self.left == 5:
                return 17
            elif self.left == 4:
                return 16
            elif self.left == 3:
                return 15
            elif self.left == 2:
                return 14
            elif self.left == 1:
                return 13
            elif self.left == 0:
                return 12
            else:
                return self.left + self.right

    # Print function of a Tile object. Prints two sides of the tile separated with ':'.
    def __str__(self):
        tile_str = "[" + str(self.left) + ":" + str(self.right) + "]"
        return tile_str

# This class represents the deck of a domino game.
# Hold the values of the tiles that did not deal to the players. While the deck is not empty, a player can draw
# new tile from the deck.
class DoubleSix:
    def __init__(self):
        self.deck = []
        self.num_tiles = 0

# This class represents the game board.
# Hold the current values that can be play and list of the tiles played already.
class LOP:
    def __init__(self):
        self.tiles = []
        self.start = 0
        self.end = 0

    # Adds the first tile in a game to the board lower value to the left.
    def add_first(self, tile):
        if tile.get_right() >= tile.get_left():
            self.start = tile.get_left()
            self.end = tile.get_right()
            self.tiles.append(tile)
        else:
            self.start = tile.get_right()
            self.end = tile.get_left()
            self.tiles.append(tile.rotate())

    # Adds new tile to the left side of the board. If the move is not legal, raise an error.
    def add_tile_start(self, tile):
        if self.start == tile.get_right():
            self.tiles.insert(0, tile)
            self.start = tile.get_left()
        elif self.start == tile.get_left():
            self.tiles.insert(0, tile.rotate())
            self.start = tile.get_right()
        else:
            raise ValueError

    # Adds new tile to the right side of the board. If the move is not legal, raise an error.
    def add_tile_end(self, tile):
        if self.end == tile.get_left():
            self.tiles.append(tile)
            self.end = tile.get_right()
        elif self.end == tile.get_right():
            self.tiles.append(tile.rotate())
            self.end = tile.get_left()
        else:
            raise ValueError

    # Prints the current state of the board.
    def print_LOP(self):
        print "LOP  ::",
        for i in xrange(0, len(self.tiles)):
            print self.tiles[i],
        print

# This class represents a domino game player.
# During initialization a player gets unique ID, Name, defined to be a human player or computer.
# If computer selected, level of player is determined.
# Each player gets a new hand of 7 tiles.
class Player:
    def __init__(self, id, name, is_human, skill, tiles):
        self.id = id
        self.name = name
        self.is_human = is_human
        self.skill = skill
        self.hand = tiles

    # Return a player ID.
    def get_id(self):
        return self.id

    # Return a player name.
    def get_name(self):
        return self.name

    # Return if player is human or computer.
    def get_is_human(self):
        return self.is_human

    # Return skill of computer player, empty string if player is human.
    def get_skill(self):
        return self.skill

    # Return number of tiles in a player hand.
    def get_tiles_num(self):
        return len(self.hand)

    # Return player hand.
    def get_hand(self):
        return self.hand

    # Prints player hand.
    def print_hand(self):
        print "Hand ::",
        for i in xrange(0, len(self.hand)):
            print self.hand[i],
        print

    # After tile was played, delete it from the player hand and adds it to the board.
    def delete_tile(self, loc):
        self.hand.pop(loc)

# This class represents a medium level computer player.
# Inherit from the class Player, medium computer have all information as regular player but uses more complex calculate
# to determine his moves.
# Hold lists of known tiles. When playing calculate the best move to do.
class MediumComp(Player):
    def __init__(self, id, name, is_human, skill, tiles):
        Player.__init__(self, id, name, is_human, skill, tiles)
        self.known = [0] * 7
        self.unknown_tiles = 28
        for i in xrange(0, len(self.hand)):
            self.known[self.hand[i].get_left()] += 1
            if self.hand[i].get_left() != self.hand[i].get_right():
                self.known[self.hand[i].get_right()] += 1
            self.unknown_tiles -= 1

# This class represents a domino game.
# Holds list of Players, DoubleSix (deck), LOP (board).
# Manage the data during the game.
class Game:
    # Constructor. Initiate new game, empty Players DoubleSix and LOP.
    def __init__(self):
        self.players = []
        self.lop = LOP()
        self.double6 = DoubleSix()

    # Parsing data file from the user. The file holds the data about how to deal tiles to players.
    def file_parser(self, file_path):

        # Read each line of file, clear it from useless lines and comments.
        with open(file_path, "r") as input_file:
            data = input_file.read()
            data = data.translate(None, ' ')
        data = re.sub(re.compile("/\*(.|[\r\n])*?\*/", re.DOTALL), "", data)
        data = re.sub(re.compile("/\*\*(.|[\r\n])*?\*/", re.DOTALL), "", data)
        data = re.sub(re.compile("\"\"\"(.|[\r\n])*?\"\"\"", re.DOTALL), "", data)
        data = re.sub(re.compile("//.*"), "", data)
        data = re.sub(re.compile("#.*"), "", data)
        data = data.strip()
        data = data.translate(None, '\r')
        data = data.split('\n')
        data = filter(None, data)
        for i in xrange(0, 4):
            data[i] = data[i].split('-')
        for j in xrange(0, 4):
            for i in xrange(0, 7):
                data[j][i] = data[j][i].split(',')

        # Return list of hands, ready to be deal to the players. for each hand, if a player gets it, contains the
        # information of indexes to put in a player hand.
        return data

    # Creates new player according to input from the user. Using the result of the parsed file to create hands.
    def add_player(self, player_id, name, is_human, skill, tiles):
        if skill == '':   # Creates human player or easy computer.
            self.players.append(Player(player_id, name, is_human, skill, tiles))
        else:             # Creates medium computer.
            self.players.append(MediumComp(player_id, name, is_human, skill, tiles))

# Prints options to play a turn.
def print_options():
    return raw_input(CHOOSE_ACTION).lower()

# If play a tile was selected, print the options to play a turn.
def print_choose_tile(tiles_num):
    tile, pos = raw_input("Choose tile (1-" + str(tiles_num) + "), and place (Start - s, End - e): ").lower().split(' ')
    return int(tile) - 1, pos

# Prints win note if one of the players has won.
def print_win(player_id, player_name):
    print "Player " + str(player_id) + ", " + player_name + " wins!"

# Prints draw note if none of the players can play.
def print_draw():
    print "It's a draw!"

# Before a turn, prints the current state of a player hand and Lop.
def print_step(player, lop):
    print "\nTurn of " + player.get_name() + " to play, player " + str(player.get_id()) + ":"
    player.print_hand()
    lop.print_LOP()

# Set a new game. Parse the file and create new players.
def game_set_up(game):
    print "Welcome to Domino!"

    file_path = raw_input("'tile' file path: ")

    # In this case, file_parser() should return iterable data structure (later we will access tiles[i])
    tiles = game.file_parser(file_path)

    num_of_players = raw_input("number of players (1-4): ")
    hand = [0] * 7
    hands = []
    counter = int(num_of_players)
    # Sort the hands of each player according to the file given by the user.
    # Puts the extra tiles as they are in the deck.
    for i in xrange(0, len(tiles)):
        for j in xrange(0, len(hand)):
            pos = int(tiles[i][j][0])
            low = min(int(tiles[i][j][1]) ,int(tiles[i][j][2]))
            high = max(int(tiles[i][j][1]) ,int(tiles[i][j][2]))
            if counter > 0:
                hand[pos - 1] = Tile(low, high)
            else:
                game.double6.deck.append(Tile(low, high))
                game.double6.num_tiles += 1
        counter -= 1
        hands.append(hand)
        hand = [0] * 7

    # Adds the new Players.
    for i in xrange(1, int(num_of_players) + 1):
        player_name, is_human = raw_input("player " + str(i) + "name: "), raw_input("Human player (y/n): ").lower()
        game.add_player(i, player_name, is_human,
                        raw_input("Computer skill: Easy (e), Medium (m): ").lower() if is_human == 'n' else "",
                        hands[i - 1])

# Finds the first player in the game.
def find_first(game):
    max = 0
    id = 0
    name = ''
    for i in xrange(0, len(game.players)):
        for j in xrange(0, 7):
            if game.players[i].hand[j].score() >= max:
                max = game.players[i].get_hand()[j].score()
                id = game.players[i].get_id()
                name = game.players[i].get_name()
            elif game.players[i].get_hand()[j].score() == max:
                if game.players[i].get_name() < name:
                    id = game.players[i].get_id()
    return id

# As the first player is determine, plays his first turn (with his first tile) automatically.
def first_turn(game, id):
    print_step(game.players[id], game.lop)
    game.lop.add_first(game.players[id].get_hand()[0])
    update_medium(game, id, game.players[id].get_hand()[0])
    game.players[id].delete_tile(0)

# Play one full turn in the game.
def play_turn(game, id):
    # Human turn. Decision made by input from user.
    if game.players[id].get_is_human() == 'y':
        # Prints turn options while valid move is not chosen.
        while True:
            option = print_options()
            try:
                if option == 't':    # Add tile
                    tile, pos = print_choose_tile(game.players[id].get_tiles_num())
                    if pos == 's':
                        game.lop.add_tile_start(game.players[id].get_hand()[int(tile)])
                    elif pos == 'e':
                        game.lop.add_tile_end(game.players[id].get_hand()[int(tile)])

                    # Updates all medium computer with the new tile that played.
                    update_medium(game, id, game.players[id].get_hand()[int(tile)])
                    game.players[id].delete_tile(int(tile))
                    break
                elif option == 'd' and game.double6.num_tiles != 0:   # Draw tile.
                    draw_tile(game, id)
                    break
            except ValueError:
                print ILLEGAL_MOVE
    else:
        # Computer turn. Decisions made by easy or medium algorithm.
        if game.players[id].get_skill() == 'e':
            easy_move(game, id)
        else:
            med_move(game, id)

# Easy computer move algorithm. Plays the first legal move by going over all the possibilities.
def easy_move(game, id):
    draw = True
    for i in xrange(0, len(game.players[id].get_hand())):
        low = game.players[id].get_hand()[i].get_left()
        high = game.players[id].get_hand()[i].get_right()
        if low == game.lop.end:
            game.lop.add_tile_end(game.players[id].get_hand()[i])
            update_medium(game, id, game.players[id].get_hand()[i])
            game.players[id].delete_tile(i)
            draw = False
            break
        elif low == game.lop.start:
            game.lop.add_tile_start(game.players[id].get_hand()[i])
            update_medium(game, id, game.players[id].get_hand()[i])
            game.players[id].delete_tile(i)
            draw = False
            break
        elif high == game.lop.end:
            game.lop.add_tile_end(game.players[id].get_hand()[i])
            update_medium(game, id, game.players[id].get_hand()[i])
            game.players[id].delete_tile(i)
            draw = False
            break
        elif high == game.lop.start:
            game.lop.add_tile_start(game.players[id].get_hand()[i])
            update_medium(game, id, game.players[id].get_hand()[i])
            game.players[id].delete_tile(i)
            draw = False
            break

    # In case of none legal move of adding a tile.
    if draw:
        draw_tile(game, id)

# Medium computer move algorithm. Plays the best move which the rivals has the lower possibility to react to.
def med_move(game, id):
    min_score = 3.0
    tile_pos = 0
    side = ''
    # Going over all the legal moves and calculates the score of it.
    for i in xrange(0, len(game.players[id].get_hand())):
        low = game.players[id].get_hand()[i].get_left()
        high = game.players[id].get_hand()[i].get_right()
        if low == game.lop.end:
            if calc_score(game, id, high) < min_score:
                min_score = calc_score(game, id, high)
                tile_pos = i
                side = 'end'
        if low == game.lop.start:
            if calc_score(game, id, high) < min_score:
                min_score = calc_score(game, id, high)
                tile_pos = i
                side = 'start'
        if high == game.lop.end:
            if calc_score(game, id, low) < min_score:
                min_score = calc_score(game, id, low)
                tile_pos = i
                side = 'end'
        if high == game.lop.start:
            if calc_score(game, id, low) < min_score:
                min_score = calc_score(game, id, low)
                tile_pos = i
                side = 'start'
    # In case of all moves score is more than 2, choose to draw a tile.
    if min_score > 2:
        draw_tile(game, id)
    elif side == 'end':
        game.lop.add_tile_end(game.players[id].get_hand()[tile_pos])
        update_medium(game, id, game.players[id].get_hand()[tile_pos])
        game.players[id].delete_tile(tile_pos)
    elif side == 'start':
        game.lop.add_tile_start(game.players[id].get_hand()[tile_pos])
        update_medium(game, id, game.players[id].get_hand()[tile_pos])
        game.players[id].delete_tile(tile_pos)

# Calculates the score of a move.
# The score of legal move is the number of the unknown tiles of the type that the new move will create,
# (which is the second part of a tile) divided by the all unknown tiles.
# Known tile is one that already played to the board or one in the player hand.
def calc_score(game, id, pos):
    return (float(7 - game.players[id].known[pos]) / game.players[id].unknown_tiles)

# Updates all of the medium computer players. After each turn, update the new known tiles for each player.
def update_medium(game, id, tile):
    for i in xrange(0, len(game.players)):
        if isinstance(game.players[i], MediumComp) and game.players[i].get_id() != id + 1:
            update_this(game, i, tile)

# Update one current medium computer player with one new tile played.
def update_this(game, id, tile):
    game.players[id].known[tile.get_left()] += 1
    if tile.get_left() != tile.get_right():
        game.players[id].known[tile.get_right()] += 1
    game.players[id].unknown_tiles -= 1

# Check if the next player can play. A player can play if he has legal moves or he can draw a tile from the deck.
# If none of the players can play, Draw is declared.
def check_next(game, id):
    for i in xrange(0, len(game.players[id].get_hand())):
        # Checks for legal move.
        if game.players[id].get_hand()[i].get_left() == game.lop.start \
                or game.players[id].get_hand()[i].get_left() == game.lop.end \
                or game.players[id].get_hand()[i].get_right() == game.lop.start \
                or game.players[id].get_hand()[i].get_right() == game.lop.end:
            return False
    return True

# Draw a tile from the deck.
def draw_tile(game, id):
    tile = Tile(game.double6.deck[0].get_left(), game.double6.deck[0].get_right())
    game.double6.deck.pop(0)
    game.players[id].get_hand().append(tile)
    game.double6.num_tiles -= 1
    if isinstance(game.players[id], MediumComp):
        update_this(game, id, tile)

# Main. Runs the game.
def main():
    game = Game()
    game_set_up(game)
    next_player_id = find_first(game)
    first_turn(game, next_player_id - 1)
    next_player_id %= len(game.players)
    next_player_id += 1
    while True:
        skipped = 0
        draw = False
        # Checks if the next player can play. If not skip this player. If none of the players can play it's a draw.
        while check_next(game, next_player_id - 1) and game.double6.num_tiles == 0:
            next_player_id %= len(game.players)
            next_player_id += 1
            skipped += 1
            if skipped == len(game.players):
                draw = True
                break
        if draw == True:
            print_draw()
            break
        print_step(game.players[next_player_id - 1], game.lop)
        play_turn(game, next_player_id - 1)
        if len(game.players[next_player_id - 1].get_hand()) == 0:
            print_win(next_player_id, game.players[next_player_id - 1].get_name())
            break

        next_player_id %= len(game.players)
        next_player_id += 1


if __name__ == "__main__":
    main()
