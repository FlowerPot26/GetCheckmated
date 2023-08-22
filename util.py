import berserk
import time

class Game:
    def __init__(self, lives=3):

        token = "lip_S5HS6N8GzcerLeeA3vNg"      # Token Definition

        self.session = berserk.TokenSession(token)
        self.client = berserk.Client(self.session)
        self.bot = berserk.clients.Bots(self.session)
        self.games = berserk.clients.Games(self.session)
        self.board = berserk.clients.Board(self.session)

        # Normal Variables:
        self.current_game_id = ""
        self.game_ongoing = True
        self.lives_left = lives

    def create_ai_game(self):
        """Aborts all ongoing Games and makes a new one"""

        all_games = self.games.get_ongoing()
        for game in all_games:
            print("Aborted Game: " + str(game.get("gameId")))
            self.bot.resign_game(str(
                game.get("gameId")
            ))
        current_ai_game = (self.client.challenges.create_ai(8, color="white"))
        self.current_game_id = current_ai_game.get("id")
        print("Started Game: " + str(self.current_game_id))

    def make_move(self, move):
        self.bot.make_move(game_id=self.current_game_id, move=move)

    def resign(self):
        self.bot.resign_game(game_id=self.current_game_id)
        return "Cheatcode activated"


    def opponent_move(self):
        my_turn = False
        while not my_turn:
            game_moves = (self.games.get_ongoing())
            if game_moves:
                for game in game_moves:

                    my_turn = game.get("isMyTurn")
            else:
                break
            time.sleep(2)
        game_moves = (self.games.get_ongoing())
        if game_moves:
            for game in game_moves:
                output_move = game.get("lastMove")
        else:
            return "NoMove"

        return output_move

    def fen_to_board(self,):
        game_moves = (self.games.get_ongoing())
        board = []

        for game in game_moves:
            fen = game.get("fen")



        for row in fen.split('/'):
            brow = ""
            for c in row:
                if c == ' ':
                    break
                elif c in '12345678':
                    brow += ('  -  ' * int(c))
                elif c == ' p':
                    brow += ' p '
                elif c == 'P':
                    brow += ' P '
                elif c > 'Z':
                    brow += (" " + str(c.upper()) + " ")
                else:
                    brow += (" " + str(c) + " ")
            board.append(brow)
        board_fmtd = ""
        for row in board:
            board_fmtd += (f"[" + row + f"]" + f"\n")

        return board_fmtd

    def check_game_running(self):
        all_games = self.games.get_ongoing()
        if not all_games:
            return False
        else:
            return True

    def stream_game(self):
        while self.game_ongoing:

            game_info = (self.games.stream_game_moves(self.current_game_id))

            for info in game_info:
                print(info)
                break

            time.sleep(5)

    def stream_moves(self):
        while self.game_ongoing:

            game_moves = (self.games.get_ongoing())


            for move in game_moves:
                print(move)
                break

            time.sleep(5)

    def stream_events(self):
        while self.game_ongoing:

            game_events = (self.board.stream_incoming_events())
            print(game_events)

            for event in game_events:
                print(event)
                break

            time.sleep(5)

