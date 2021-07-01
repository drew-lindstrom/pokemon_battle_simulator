from player import Player
from pokemon import Pokemon
from move import Move
from frame import Frame
from terrain import Terrain
from weather import Weather
from damage_calc import *
from move_effects import *
from post_attack import *
from switch_effects import *
from util import *
from teams import p1, p2
import ui
import ai
import gameText

from flask import Flask, request, render_template

app = Flask(__name__)

gameOverBool = False
w = Weather()
t = Terrain()


@app.route("/")
def index():
    playerInput = request.args.get("playerInput", "")
    gameText.output = []
    if playerInput:
        frame1, frame2 = applyPreInputPreparations(p1, p2, w, t)
        ui.callAppropriateFunctionBasedOnChoice(frame1, playerInput)
        ai.chooseHighestDamagingAttack(frame2)
        if applyTurn(frame1, frame2, gameOverBool):
            ui.printOptions(frame1)
            return render_template("home.html", gameText=gameText)
        else:
            return "Game Over"

    else:
        frame1, frame2 = activateTurnOneSwitchAbilities(p1, p2, w, t)
        ui.printPokemonOnField(frame1, frame2)
        ui.printOptions(frame1)
        return render_template("home.html", gameText=gameText)


def applyTurn(frame1, frame2, gameOverBool):
    # Determines which player goes first for the turn (based on speed, priority moves, etc.)
    frameOrder = getFrameOrder(frame1, frame2)

    for curFrame in frameOrder:
        if curFrame.switchChoice:
            applySwitch(curFrame, frame1, frame2)

        elif curFrame.user.status[0] != "Fainted":
            gameText.output.append(f"{curFrame.user.name} used {curFrame.attack.name}!")

            if checkIfCanAttackAndAttackLands(curFrame):
                applyAttack(curFrame)

    gameOverBool = applyEndOfTurnEffects(frameOrder, w, t, gameOverBool)

    if gameOverBool:
        return False
    return True


def activateTurnOneSwitchAbilities(p1, p2, w, t):
    #'Switches' leading pokemon with their respective selves in order to activate any abilities that activate on switch in.
    openingFrame1 = Frame(p1, p2, None, None, w, t)
    openingFrame1.switchChoice = 0
    openingFrame2 = Frame(p2, p1, None, None, w, t)
    openingFrame2.switchChoice = 0
    switch(openingFrame1, printSwitchText=False)
    switch(openingFrame2, printSwitchText=False)
    return openingFrame1, openingFrame2


def applyPreInputPreparations(p1, p2, w, t):
    frame1 = Frame(p1, p2, None, None, w, t)
    frame2 = Frame(p2, p1, None, None, w, t)

    gameTextList = []
    frame1.gameText = gameTextList
    frame2.gameText = gameTextList

    frame1.user.checkChoiceItem()
    frame2.user.checkChoiceItem()

    return frame1, frame2


def applySwitch(curFrame, frame1, frame2):
    switch(curFrame)
    frame1.updateCurPokemon()
    frame2.updateCurPokemon()


def checkIfCanAttackAndAttackLands(frame):
    checkCanAttack(frame)
    checkAttackLands(frame)
    return frame.canAttack and frame.attackLands


def applyAttack(frame):
    category = frame.attack.category

    if category == "Physical" or category == "Special":
        frame.attackDamage = calcDamage(frame)
        frame.target.applyDamage(frame.attackDamage, None)
    else:
        applyNonDamagingMove(frame)

    applyPostAttackEffects(frame)


def applyEndOfTurnEffects(frameOrder, w, t, gameOverBool):
    applyEndOfTurnAttackEffects(frameOrder)

    w.decrementWeather()
    t.decrementTerrain()

    if checkForGameOver(frameOrder):
        gameOverBool = True
        return gameOverBool

    checkForFaintedPokemon(frameOrder)
    return gameOverBool


def checkForGameOver(frameOrder):
    for curFrame in frameOrder:
        player = curFrame.attackingTeam
        if player.checkGameOver():
            if player == p1:
                gameText.output.append("Player 2 Wins!")
            elif player == p2:
                gameText.output.append("Player 1 Wins!")
            return True
    return False


def checkForFaintedPokemon(frameOrder):
    for curFrame in frameOrder:
        player = curFrame.attackingTeam
        if player.curPokemon.status[0] == "Fainted":
            getAppropriateSwitchChoice(curFrame)
            switch(curFrame, printSwitchText=True, printStatResetText=False)


def getAppropriateSwitchChoice(frame):
    player = frame.attackingTeam
    if player == p1:
        ui.getSwitch(frame)
    if player == p2:
        ai.chooseNextPokemon(frame)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)