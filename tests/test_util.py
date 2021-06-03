from util import *
from player import Player
from move import Move
from pokemon import Pokemon
from weather import Weather
from terrain import Terrain
from frame import Frame

import pytest


class TestUtil:
    @pytest.fixture
    def test_pokemon(self):
        test_pokemon = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        return test_pokemon

    @pytest.fixture
    def test_frame(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            "Regenerator",
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        tapu_lele = Pokemon(
            "Tapu Lele",
            100,
            None,
            ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
            "Psychic Surge",
            "Choice Specs",
            (31, 0, 31, 31, 31, 31),
            (0, 0, 0, 252, 4, 252),
            "Timid",
        )
        cinderace = Pokemon(
            "Cinderace",
            100,
            "Male",
            ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
        )
        p1 = Player([slowbro, tyranitar])
        p2 = Player([tapu_lele, cinderace])
        w = Weather()
        t = Terrain()
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    @pytest.fixture
    def test_frame2(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        tapu_lele = Pokemon(
            "Tapu Lele",
            100,
            None,
            ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
            "Psychic Surge",
            "Choice Specs",
            (31, 0, 31, 31, 31, 31),
            (0, 0, 0, 252, 4, 252),
            "Timid",
        )
        cinderace = Pokemon(
            "Cinderace",
            100,
            "Male",
            ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
        )
        p1 = Player([tapu_lele, cinderace])
        p2 = Player([slowbro, tyranitar])
        w = Weather()
        t = Terrain()
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    def test_get_frame_order(self):
        test_pokemon_1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 252, 0, 4, 252),
            "Relaxed",
        )

        test_pokemon_2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        player1 = Player([test_pokemon_1])
        player2 = Player([test_pokemon_2])
        t = Terrain()
        f1 = Frame(player1, player2, None, None, None, t)
        f2 = Frame(player2, player1, None, None, None, t)

        f1.attack_name = "Pursuit"
        f2.switch_choice = 1
        assert get_frame_order(f1, f2) == [f1, f2]
        f1.attack_name = "Tackle"
        f2.switch_choice = None
        f2.attack_name = "Pursuit"
        assert get_frame_order(f1, f2) == [f1, f2]
        f1.attack_name = None
        f1.switch_choice = 1
        f2.attack_name = None
        f2.switch_choice = 1
        assert get_frame_order(f1, f2) == [f1, f2]
        f1.switch_choice = None
        f1.attack_name = "Tackle"
        assert get_frame_order(f1, f2) == [f2, f1]
        f2.switch_choice = None
        f2.attack_name = "Extreme Speed"
        assert get_frame_order(f1, f2) == [f2, f1]
        f1.attack_name = "Teleport"
        f2.attack_name = "Tackle"
        assert get_frame_order(f1, f2) == [f2, f1]
        f1.attack_name = "Extreme Speed"
        f2.attack_name = "Extreme Speed"
        assert get_frame_order(f1, f2) == [f1, f2]
        f1.user.status = ["Paralyzed"]
        f1.attack_name = None
        f1.switch_choice = 1
        f2.attack_name = None
        f2.switch_choice = 1
        assert get_frame_order(f1, f2) == [f2, f1]
        f1.switch_choice = None
        f1.attack_name = "Tackle"
        f2.switch_choice = None
        f2.attack_name = "Tackle"
        assert get_frame_order(f1, f2) == [f2, f1]

    def test_check_speed(self):
        test_pokemon_1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )

        test_pokemon_2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        player1 = Player([test_pokemon_1])
        player2 = Player([test_pokemon_2])
        f1 = Frame(player1, player2, None, None, None, None)
        f2 = Frame(player2, player1, None, None, None, None)
        assert check_speed(f1, f2) == [f2, f1]
        f1.user.status[0] = "Paralyzed"
        assert check_speed(f1, f2) == [f2, f1]
        f1.user.status[0] = None
        f1.user.stat_mod["speed"] = 4
        assert check_speed(f1, f2) == [f1, f2]
        f1.user.status[0] = "Paralyzed"
        assert check_speed(f1, f2) == [f1, f2]
        f1.user.status[0] = None
        f1.user.stat_mod["speed"] = -4
        assert check_speed(f1, f2) == [f2, f1]

        test_pokemon_1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 252, 0, 0, 252),
            "Relaxed",
        )
        player1 = Player([test_pokemon_1])
        player2 = Player([test_pokemon_2])
        f1 = Frame(player1, player2, None, None, None, None)
        f2 = Frame(player2, player1, None, None, None, None)
        f1.user.stat_mod["speed"] = 0
        assert check_speed(f1, f2) == [f1, f2]
        f1.user.status[0] = "Paralyzed"
        assert check_speed(f1, f2) == [f2, f1]
        f1.user.status[0] = None
        f1.user.stat_mod["speed"] = 4
        assert check_speed(f1, f2) == [f1, f2]
        f1.user.stat_mod["speed"] = -4
        assert check_speed(f1, f2) == [f2, f1]

        test_pokemon_1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        test_pokemon_2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 252),
            "Relaxed",
        )
        player1 = Player([test_pokemon_1])
        player2 = Player([test_pokemon_2])
        f1 = Frame(player1, player2, None, None, None, None)
        f2 = Frame(player2, player1, None, None, None, None)
        f1.user.stat_mod["speed"] = 0
        assert check_speed(f1, f2) == [f2, f1]
        f1.user.stat_mod["speed"] = 4
        assert check_speed(f1, f2) == [f1, f2]
        f1.user.stat_mod["speed"] = -4
        assert check_speed(f1, f2) == [f2, f1]

    def test_check_priority(self, test_frame):
        test_frame.terrain.current_terrain = "Grassy Terrain"
        test_frame.attack_name = "Ice Shard"
        assert check_priority(test_frame) == 1
        test_frame.attack_name = "Avalanche"
        assert check_priority(test_frame) == -4
        test_frame.attack_name = "Tackle"
        assert check_priority(test_frame) == 0
        test_frame.attack_name = "Grassy Glide"
        assert check_priority(test_frame) == 1
        test_frame.terrain.current_terrain = "Psychic Terrain"
        test_frame.attack_name = "Ice Shard"
        assert check_priority(test_frame) == 0

    def test_roll_paralysis(self, test_pokemon):
        assert roll_paralysis(test_pokemon, 4) == True
        assert roll_paralysis(test_pokemon, 1) == False

    def test_roll_frozen(self, test_pokemon):
        test_pokemon.status[0] = "Frozen"
        assert roll_frozen(test_pokemon, 4) == False
        assert test_pokemon.status[0] == "Frozen"
        assert roll_frozen(test_pokemon, 1) == True
        assert test_pokemon.status[0] == None

    def test_roll_confusion(self, test_pokemon):
        assert roll_confusion(test_pokemon, 2) == True
        assert roll_confusion(test_pokemon, 1) == False

    @pytest.mark.parametrize(
        "attack_type,target_type,expected",
        [
            ("Poison", "Steel", False),
            ("Dragon", "Fairy", False),
            ("Normal", "Ghost", False),
            ("Fighting", "Ghost", False),
            ("Ghost", "Normal", False),
            ("Electric", "Ground", False),
            ("Psychic", "Dark", False),
            ("Poison", "Fire", True),
        ],
    )
    def test_check_immunity(self, test_frame, attack_type, target_type, expected):
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack.type = attack_type
        test_frame.target.typing[0] = target_type
        assert check_immunity(test_frame) == expected

    def test_check_can_attack(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        test_frame.user.status = ["Paralyzed", 2]
        assert check_can_attack(test_frame, 1) == False
        assert check_can_attack(test_frame, 2) == True
        test_frame.user.status = ["Asleep", 3]
        assert check_can_attack(test_frame) == False
        test_frame.user.status = ["Frozen", 3]
        assert check_can_attack(test_frame, 2) == False

        test_frame.user.status = [None]
        test_frame.user.v_status["Flinched"] = [2]
        assert check_can_attack(test_frame) == False
        del test_frame.user.v_status["Flinched"]
        test_frame.user.v_status["Confusion"] = [1]
        assert check_can_attack(test_frame, 1) == False
        del test_frame.user.v_status["Confusion"]
        test_frame.attack.type = "Poison"
        test_frame.target.typing[0] = "Steel"
        assert check_can_attack(test_frame) == False
        test_frame.target.typing[0] = "Water"
        assert check_can_attack(test_frame) == True
        test_frame.target.ability = "Flash Fire"
        test_frame.attack.type = "Fire"
        assert check_can_attack(test_frame) == False
        assert test_frame.target.stat_mod["attack"] == 1
        assert test_frame.target.stat_mod["sp_attack"] == 1

    def test_check_attack_lands(self, test_frame, test_frame2):
        test_frame.attack = test_frame.user.moves[1]
        check_attack_lands(test_frame)
        assert test_frame.attack_lands == True
        test_frame2.attack = test_frame2.user.moves[2]
        check_attack_lands(test_frame2, 100)
        assert test_frame2.attack_lands == False
        check_attack_lands(test_frame2, 20)
        assert test_frame2.attack_lands == True
        test_frame2.attack_name = "High Jump Kick"
        check_attack_lands(test_frame2, 100)
        assert test_frame2.user.stat["hp"] == 140

    def test_apply_non_damaging_move(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack_name = "Stealth Rocks"
        apply_non_damaging_move(test_frame)
        assert test_frame.defending_team.stealth_rocks == True
        test_frame.attack_name = "Defog"
        apply_non_damaging_move(test_frame)
        assert test_frame.defending_team.stealth_rocks == False

    def test_switch(self, test_frame):
        # TODO: Needs to be updated.
        test_frame.user.prev_move = "Scald"
        test_frame.user.stat_mod["attack"] = 6
        test_frame.user.v_status["Confused"] = [0]
        test_frame.user.stat["hp"] = 50
        test_frame.attacking_team.stealth_rocks = True
        test_frame.switch_choice = 1
        switch(test_frame)
        test_frame.update_cur_pokemon()
        assert test_frame.user.name == "Tyranitar"
        assert test_frame.user.stat["hp"] == 353
        assert test_frame.attacking_team[1].prev_move == None
        assert test_frame.attacking_team[1].stat_mod["attack"] == 0
        assert len(test_frame.attacking_team[1].v_status) == 0
        assert test_frame.attacking_team[1].stat["hp"] == 181
        test_frame.attacking_team[1].stat["hp"] = 0
        switch(test_frame)
        test_frame.update_cur_pokemon()
        assert test_frame.user.name == "Tyranitar"

    def test_apply_switch_effect(self, test_frame):
        test_frame.user.ability = "Grassy Surge"
        apply_switch_effect(test_frame, 0, "In")
        assert test_frame.terrain.current_terrain == "Grassy Terrain"
        test_frame.terrain.current_terrain = None
        test_frame.user.ability = "Psychic Surge"
        apply_switch_effect(test_frame, 0, "In")
        assert test_frame.terrain.current_terrain == "Psychic Terrain"
        test_frame.user.ability = "Intimidate"
        apply_switch_effect(test_frame, 0, "In")
        assert test_frame.target.stat_mod["attack"] == -1
        test_frame.user.ability = "Sand Stream"
        apply_switch_effect(test_frame, 0, "In")
        assert test_frame.weather.current_weather == "Sandstorm"
        test_frame.user.stat["hp"] = 50
        test_frame.user.ability = "Regenerator"
        apply_switch_effect(test_frame, 0, "Out")
        assert test_frame.user.stat["hp"] == 181

    def test_apply_entry_hazards(self, test_frame):
        test_frame.attacking_team.stealth_rocks = True
        apply_entry_hazards(test_frame)
        assert test_frame.user.stat["hp"] == 344
        test_frame.user.item = "Heavy Duty Boots"
        apply_entry_hazards(test_frame)
        assert test_frame.user.stat["hp"] == 344

    def test_apply_stealth_rocks_damage(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        charizard = Pokemon(
            "Charizard",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        fearow = Pokemon(
            "Fearow",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        aggron = Pokemon(
            "Aggron",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        steelix = Pokemon(
            "Steelix",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        test_player = Player([slowbro, aggron, steelix, fearow, charizard])
        test_frame = Frame(test_player, test_player, None, None, None, None)
        apply_stealth_rocks_damage(test_frame)
        assert test_frame.user.stat["hp"] == 289
        test_frame.user = aggron
        apply_stealth_rocks_damage(test_frame)
        assert test_frame.user.stat["hp"] == 263
        test_frame.user = steelix
        apply_stealth_rocks_damage(test_frame)
        assert test_frame.user.stat["hp"] == 281
        test_frame.user = fearow
        apply_stealth_rocks_damage(test_frame)
        assert test_frame.user.stat["hp"] == 203
        test_frame.user = charizard
        apply_stealth_rocks_damage(test_frame)
        assert test_frame.user.stat["hp"] == 148

    def test_apply_post_attack_effects(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Close Combat", "Toxic", "Test Dark Pulse", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        team1 = Player([slowbro])
        team2 = Player([tyranitar])
        test_frame = Frame(team1, team2, None, None, None, None)
        test_frame.attack = test_frame.user.moves[0]
        assert test_frame.user.stat_mod["defense"] == 0
        assert test_frame.user.stat_mod["sp_defense"] == 0
        apply_post_attack_effects(test_frame)
        assert test_frame.user.stat_mod["defense"] == -1
        assert test_frame.user.stat_mod["sp_defense"] == -1
        test_frame.attack = test_frame.user.moves[1]
        assert test_frame.target.status[0] == None
        apply_post_attack_effects(test_frame)
        assert test_frame.target.status[0] == "Badly Poisoned"
        test_frame.attack = test_frame.user.moves[2]
        assert len(test_frame.target.v_status) == 0
        apply_post_attack_effects(test_frame)
        assert test_frame.target.v_status["Flinched"] == [1]

    def test_apply_end_of_turn_effects(self, test_frame, test_frame2):
        frame_order = [test_frame, test_frame2]
        test_frame.attack = test_frame.user.moves[0]
        test_frame2.attack = test_frame2.user.moves[0]
        test_frame.weather.current_weather = "Sandstorm"
        test_frame.user.status = ["Asleep", 3]
        test_frame.user.v_status["Flinched"] = [2]
        apply_end_of_turn_effects(frame_order)
        assert test_frame.user.moves[0].pp == 23
        assert test_frame.user.stat["hp"] == 369
        assert test_frame.user.status[1] == 2
        assert test_frame.user.v_status["Flinched"] == [1]
        test_frame.user.stat["hp"] = 50
        test_frame.weather.current_weather = None
        test_frame.terrain.current_terrain = "Grassy Terrain"
        test_frame2.user.status = ["Burned", 1]
        apply_end_of_turn_effects(frame_order)
        assert test_frame.user.stat["hp"] == 74
        assert test_frame2.user.stat["hp"] == 263
        test_frame.terrain.current_terrain = None
        test_frame.user.item = "Leftovers"
        test_frame2.user.status = ["Badly Poisoned", 3]
        apply_end_of_turn_effects(frame_order)
        assert test_frame.user.stat["hp"] == 98
        assert test_frame2.user.stat["hp"] == 34
        test_frame2.user.status = ["Poisoned", 4]
        test_frame2.user.stat["hp"] = 200
        apply_end_of_turn_effects(frame_order)
        assert test_frame2.user.stat["hp"] == 164
        test_frame.attack_name = "Wood Hammer"
        test_frame.attack_damage = 100
        assert test_frame.user.stat["hp"] == 122
