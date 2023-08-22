from flask import Flask, render_template, request, redirect, url_for, g, session , abort
import util
import berserk

app = Flask(__name__)
app.secret_key = "hehehaha"
app.session = None
app.last_move = ""
app.opponent_move = ""
app.error = ""
app.win = False

@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input == "start" or user_input == "start2":

            """variable definitions"""
            need_help = False
            game_ongoing = True
            win = False

            """global definition of instance of Game"""
            new_game = util.Game()
            new_game.create_ai_game()
            app.session = new_game
            app.last_move = ""
            app.opponent_move = ""
            app.error = ""
            app.win = False

        return redirect("/game/move")
    return render_template("start.html")


@app.route("/game/move",methods=["GET","POST"])
def game_move():
    new_game = app.session
    if request.method == "POST":

        try:
            move_input = request.form.get("move_input")
            app.last_move = move_input
            app.error = ""

            if new_game:
                if move_input == "cheatcode":
                    new_game.resign()
                else:
                    new_game.make_move(move_input)
                app.opponent_move = str(new_game.opponent_move())
                if app.opponent_move == "NoMove":
                    app.win = True
                    return redirect("/game/win")

        except berserk.exceptions.ResponseError as e:
            app.error = "Error:" + str(e) + "\n\n" + new_game.fen_to_board() + "\nTry again!"
            app.last_move = ""


    if new_game:
        return render_template("move.html", last_move=app.last_move, opponent_move = app.opponent_move, error=app.error)
    else:
        return "Start a game first please"



@app.route("/game/win")
def win():
    if app.win:
        return render_template("win.html")
    abort(401)
    return "Nope"
