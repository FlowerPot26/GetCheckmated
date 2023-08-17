import berserk
import util





# Main LOOP
while True:
    player_input = input("""Write "start" to start \nWrite "start2" to start with help \nWrite "exit" to exit \n-""")
    if player_input == "start" or player_input == "start2":
        need_help = False
        game_ongoing = True
        win = False
        new_game = util.Game()
        new_game.create_ai_game()
        if player_input == "start2":
            need_help = True


        while game_ongoing:
            if win:
                print("Congratulations, you win!")
                break
            elif new_game.lives_left <= 0:
                print("No lives left, you lose!")
                break
            else:

                while True:
                    if new_game.check_game_running():
                        if new_game.lives_left > 0:
                            try:
                                move_input = input("Enter your next move: ")
                                if move_input == "cheatcode":
                                    print(new_game.resign())
                                else:
                                    new_game.make_move(move_input)
                                    print("Move made!")

                                if new_game.check_game_running():
                                    opponent_move = str(new_game.opponent_move())
                                    if opponent_move == "NoMove":
                                        win = True
                                        break
                                    print("Opponent move: " + opponent_move)
                                    if need_help == True:
                                        print(new_game.fen_to_board())
                                break
                            except berserk.exceptions.ResponseError as e:
                                print("Error: " + str(e) + ", try again!")
                                new_game.lives_left += -1

                                if new_game.lives_left > 0:
                                    print("Lives left: " + str(new_game.lives_left))
                                    if not need_help:
                                        print(new_game.fen_to_board())
                        else:
                            break
                    else:

                        win = True
                        break



    elif player_input == "exit":
        break
    else:
        print("Invalid Input")