from pokemon import player, enemy
from dialogbox import dialogbox
from sprite import sprite

class menu:
    """Basic (parent) menu class."""
    def __init__(self,input_text=None):
        """
        Creates a menu

        :param input_text: text to show when asking for input
        """
        # Text to show when asking for user input
        if input_text != None:
            self.input_text = input_text
        else:
            self.input_text = "Select an action: "

        self.menu_content = []              # Menu content to render
        self.dialog = dialogbox(border=2)   # Dialogbox


    def show_and_select(self):
        """
        Function to show the menu and select menu action choices.

        :return: Menu selection
        """
        self.render()
        choice = input(self.input_text)

        # Check wether input is a digit and is a valid choice
        while not choice.isdigit() or (not 0 <= int(choice) < len(self.actions)):
            self.render()
            print(f"Please show a valid option (0 - {len(self.actions)-1}).")
            choice = input(self.input_text)
        
        print()
        action = self.actions[int(choice)]
        return action

    def render(self):
        """Function to render menu elements (pokemons, dialog, title)."""
        print("\n".join(self.menu_content))
        self.dialog.show()
        
    def to_choice(self, text, ind = None):
        """
        Function to convert a list of actions or action (with given index) to
        a choice format.

        :param text: List of lines or string (with index) to convert to choice format
        :param ind: Index of choice (if text is a string)
        :return: text in choice format
        """
        if type(text) == list and ind == None:
            return [f"{i} - {a}" for i,a in enumerate(text)] 
        else:
            return f"{ind} - {text}"

class MainMenu(menu):
    """Main menu class."""
    def __init__(self):
        """Creates a main menu."""
        # Define action choices
        self.actions = ["Play","Exit"]

        super().__init__()

        # Define dialog text and menu render content
        dialog_text = self.to_choice(self.actions)
        title = sprite('Title')
        self.width = title.width
        self.dialog(dialog_text)
        self.dialog.center(self.width)
        self.menu_content = [title.text]


class SelectionMenu(menu):
    """Pokemon selection class."""
    def __init__(self,pokemons,sprites,is_player):
        """
        Creates a Pokemon selection menu.

        :param pokemons: Pokemons to be selected from
        :param sprites: Corrseponding Pokemon sprites
        :param is_player: bool for checking if player or enemy
        """
        self.is_player = is_player
        
        # Define action choices
        if self.is_player:
            self.actions = [player(name,pokemons[name],sprites[ind]) for ind,name in enumerate(pokemons)]
        else:
            self.actions = [enemy(name,pokemons[name],sprites[ind]) for ind,name in enumerate(pokemons)]
        
        # Define dialog text, input text and menu content
        input_text = "Select a Pokemon: " if is_player else "Select an enemy Pokemon: "
        super().__init__(input_text)
        for i,action in enumerate(self.actions):
            action_sprite = action.get_sprite(moves=True,spacing=4)
            self.menu_content.append(f"{self.to_choice(action.name,i)}\n\n{action_sprite.text}")

    def swap(self, pokemon):
        """
        Function to swap main pokemon.

        :param pokemon: Current pokemon (to update in list)
        :return: Selected pokemon to swap to
        """
        self.menu_content = []
        for ind,action in enumerate(self.actions):
            # Update current pokemon in Pokemon list
            if action.name == pokemon.name:
                self.actions[ind] = pokemon

            action_sprite = action.get_sprite(moves=True,spacing=4)
            self.menu_content.append(f"{self.to_choice(action.name,ind)}\n\n{action_sprite.text}")    
        return self.show_and_select()     

class FightMenu(menu):
    """Pokemon fight menu class."""
    def __init__(self):
        """Creates a fight menu"""
        self.player_turn = True         # bool for turn
        
        super().__init__()

    def attack_message(self,pokemon,attack):
        """
        Function thet shows an attack message.

        :param pokemon: Pokemon that used an attack
        :param attack: Attack used by pokemon
        """
        input_text = "Press enter to continue."
        self.dialog([f"{pokemon.name} used {attack}", "It was effective."])
        self.dialog.center(self.width)
        self.render()
        input(input_text)

    def battle(self, Player, Enemy):
        """
        Function that allows two pokemon to each use one attack on each other
        
        :Param Player: Playable Pokemon
        :param Enemy: Enemy (AI) Pokemon
        """

        # Define menu content
        battle_sprite = Player.render_in_battle(Enemy)
        self.menu_content = [battle_sprite.text]
        
        self.width = battle_sprite.width

        if self.player_turn:
            # Define action choices
            self.actions = list(Player.attacks.keys()) + ["Change Pokemon"]

            # Define dialog text
            actions_dialog = []
            for ind, action in enumerate(self.actions):
                action_as_choice = self.to_choice(action,ind)  # convert action to choice format
                # Put every 2 action choices on the same line
                if ind % 2 == 0 and ind < len(self.actions)-1:
                    next_action_choice = self.to_choice(self.actions[ind+1],ind+1)
                    actions_dialog.append(f"{action_as_choice}{' '*5}{next_action_choice}")
                # Add last action choice if uneven amount
                elif ind == len(self.actions)-1:
                    actions_dialog.append(action_as_choice)
            
            self.dialog(actions_dialog)
            self.dialog.center(self.width)

            # Choose attack
            choice = self.show_and_select()

            # Attack
            if choice != self.actions[-1]:
                Enemy = Player.attack(choice,Enemy)
                self.attack_message(Player,choice)

                if Enemy.hp < 0:
                    Enemy.hp = 0

                # Define menu content
                battle_sprite = Player.render_in_battle(Enemy)
                self.menu_content = [battle_sprite.text]

                # swap player
                self.player_turn = not self.player_turn
        else:
            # Attack
            Player, choice = Enemy.attack(Player)
            if Player.hp < 0:
                Player.hp = 0

            # Define menu content
            battle_sprite = Player.render_in_battle(Enemy)
            self.menu_content = [battle_sprite.text]
            self.attack_message(Enemy, choice)
            self.player_turn = not self.player_turn
        return choice == self.actions[-1]

class GameOver(menu):
    """Game over menu"""
    def __init__(self, winner):
        """
        Creates a Game Over menu

        :param winner: Pokemon that won the batle
        """
        self.actions = ["Play again","Exit"]
        super().__init__()
        text = "You Win!" if type(winner) == player else "You Lose!"
        Win_dialog = [text,""] + self.to_choice(self.actions)
        self.dialog(Win_dialog)
        self.dialog.center(winner.sprite.width)
        self.menu_content = [winner.get_sprite(hp=False).text]
