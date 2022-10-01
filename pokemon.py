import random
from sprite import sprite

class pokemon:
    """Pokemon class."""
    def __init__ (self, name, stats):
        """
        Creates a Pokemon.

        :param name: Pokemon name
        :param stats: Pokemon stats
        """
        self.name = name                # Pokemon name
        self.hp = stats['HP']           # Pokemon health
        self.attacks = stats["moves"]   # Pokemon attacks

    def get_sprite(self,hp=True,moves=False,spacing = None) :
        """
        Function to get Pokemon's sprite (with stats if needed)

        :param hp: Bool for returning hp
        :param moves: Bool for returning moves
        :param spacing: Space before sprite
        :return: Sprite (with stats)
        """
        # Return sprite without stats
        if hp == moves == False and spacing == None:
            return(self.sprite)
        # Load sprites stored spacing (if not given)
        if spacing == None:
            spacing = self.sprite.spacing

        attack_names = list(self.attacks.keys())
        sprite_lines = self.sprite.lines.copy()
        if hp:
            sprite_lines.append(f"HP: {self.hp}")
        if moves:
            sprite_lines.append(f"Moves: {', '.join(attack_names)}")
        new_sprite = sprite(lines = sprite_lines,spacing=spacing)
        return new_sprite

    def render_in_battle(self, enemy, distance=10):
        """
        Function that renders 2 pokemon in battle.

        :param enemy: enemy to render
        :param distance: distance between pokemon in battle
        :return: Sprite of 2 pokemon in battle
        """
        player_sprite = self.get_sprite()
        enemy_sprite = enemy.get_sprite()
        return(player_sprite.join(enemy_sprite,distance))

    def do_attack(self,attack,attackee):
        """
        Function to perform a certain attack on an enemy

        :param attack: attack to use
        :param attackee: enemy to use attack on
        :return: enemy with updated hp
        """
        attackee.hp -= self.attacks[attack]
        return attackee


class player (pokemon):
    """Player class"""
    def __init__(self,name, stats, sprite):
        """
        Creates a playable pokemon

        :param name: Pokemon name
        :param stats: Pokemon stats
        :param sprite: Pokemon sprite
        """
        # flip to face enemy
        self.sprite = sprite.flip()

        super().__init__(name,stats)

    def attack(self,attack,attackee):
        """
        Function to perform a player-selected attack on an enemy.

        :param attack: attack to use
        :param attackee: enemy to use attack on
        :return: enemy with updated hp
        """
        return(self.do_attack(attack,attackee))

class enemy (pokemon):
    """Enemy class"""
    def __init__(self,name, stats, sprite):
        """
        Creates a pokemon AI

        :param name: Pokemon name
        :param stats: Pokemon stats
        :param sprite: Pokemon sprite
        """
        self.sprite = sprite
        super().__init__(name, stats)

    def attack(self,attackee):
        """
        Function to perform a random attack on an enemy.

        :param attack: attack to use
        :param attackee: enemy to use attack on
        :return: enemy with updated hp
        """
        index = random.randint(0,len(self.attacks)-1)
        attack = list(self.attacks.keys())[index]
        return self.do_attack(attack,attackee),attack
        


# with open("pokemon/charmander", "r") as f:
#     # lines.
#     text = f.read()
#     # print(repr(text))
# lines = text.split('\n')
# # print(max_length)
# max_length = 0
# for ind,line in enumerate(lines):
#     if (line.count('▀') + line.count(' ') > max_length):
#         max_length = line.count('▀') + line.count(' ')
# for ind,line in enumerate(lines):
#     if len(line) < max_length:
#         lines[ind] = line + ' '*(max_length-len(line))

# print(("\n".join(lines)))
# for ind,t in enumerate(lines):
#     t = t.replace("\x1b",' ')
#     t = t.split(" ")
    
#     indices = np.where(np.array(t) == '[0m')[0]
    
#     print(t)
#     for i in indices:
#         temp = t[i]
#         t[i] = t[i-2]
#         t[i-2] = temp

#     lines[ind] = ''.join(["\x1b"+c if c.startswith('[') else " "+c for c in t[::-1]] )
# print(("\n".join(lines)))


    