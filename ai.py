from frame import Frame
import ui
import util
import damage_calc


def chooseHighestDamagingAttack(frame):
    """Returns a move index for user's highest damaging attack against the current target."""
    highestDamage = -float("inf")
    moveNumber = None
    includeCrit = False
    includeRandom = False

    for n in range(len(frame.user.moves)):
        moveCategory = frame.user.moves[n].category
        if (
            moveCategory == "Physical" or moveCategory == "Special"
        ) and ui.checkIfValidChoice(frame, n + 1):
            # ui.checkIfValidChoice subtracts 1 from the given int due to first attack being tied with '1' key.
            frame.attack = frame.user.moves[n]
            if util.checkImmunity(frame):
                damage = damageCalc.calcDamage(frame, includeCrit, includeRandom)
                if damage > highestDamage:
                    highestDamage = damage
                    moveNumber = n
    if moveNumber is None:
        chooseNextPokemon(frame)
        frame.attack = None
    else:
        frame.attack = frame.user.moves[moveNumber]

    return frame


def chooseNextPokemon(frame):
    for n in range(1, 6):
        if frame.attackingTeam[n].status[0] != "Fainted":
            frame.switchChoice = n
