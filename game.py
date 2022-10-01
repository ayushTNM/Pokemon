import json
from menu import *

class game:
    """Pokemon game class"""
    def __init__(self):
        """Function to initialize the Pokemon game."""
        with open('pokemon.json') as pokemon_data:
            self.pokemons = json.load(pokemon_data)     # Load pokemons from json file

    def loop(self):
        """Function to run the Pokemon game"""
        while True:
            # Main menu
            main = MainMenu()
            if main.show_and_select() == "Exit":   # Exit
                break
            else:
                pokemon_names = list(self.pokemons.keys())
                sprites = [sprite(name) for name in pokemon_names] # Load sprites
                # Select player
                player_select = SelectionMenu(self.pokemons,sprites,True)
                player = player_select.show_and_select()

                # Select enemy
                enemy_select = SelectionMenu(self.pokemons,sprites,False)
                enemy = enemy_select.show_and_select()
                
                # Create battle
                fight = FightMenu()

                # Battle
                while not (player.hp == 0 or enemy.hp == 0):
                    Change_pokemon = fight.battle(player,enemy)
                    # Change pokemon
                    if Change_pokemon:
                        player = player_select.swap(player)

                # Game over
                winner = max([player,enemy],key=lambda y: y.hp)
                Game_over = GameOver(winner)

                if Game_over.show_and_select() == "Exit":  # Exit
                    break

        print("Thanks for playing")