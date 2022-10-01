import os
import numpy as np

class sprite:
    """Class for loading and displaying ANSI escape code sprites"""
    def __init__(self,name=None, lines = None, spacing=0):
        """
        Creates a sprite.

        :param name: Name of sprite located in sprites folder
        :param lines: Lines of sprite
        :param spacing: Space before sprite
        """
        self.spacing = spacing      # Space before sprite

        # sprite in sprites path
        if name != None:
            self.path = f'sprites/{name.lower()}'
            if self.load_path():
                self.render()

        # sprite's lines in lines parameter
        if lines != None:
            self.lines = lines
            self.render()

    def load_path(self):
        """
        Function that loads the path of sprite.

        :return: True if loaded succesfully, false otherwise
        """
        if os.path.exists(self.path):
            with open(self.path) as sprite_file:
                self.lines = sprite_file.read().split('\n')
            return True
        else:
            print(f"Sprite '{os.path.split(self.path)[-1]}' not found")
            return False
    
    def render(self):
        """Function that renders an ANSI sprite given it's lines."""

        # Calculate sprite width
        self.width = 0
        for line in self.lines:
            line_len = line.count('▀') + line.count('▄') + line.count(' ')
            if (line_len > self.width ):
                self.width  = line_len + self.spacing

        # Add spaces before and after each line (so it is flippable)
        for ind,line in enumerate(self.lines):
            line = ' '*self.spacing + line
            if len(line) < self.width:
                line = line + ' '*(self.width-len(line))
            self.lines[ind] = line

        self.text = "\n".join(self.lines) + "\n"    # Sprite represented in text


    def flip(self):
        """Function that flip the current sprite forizontally."""
        flipped_lines = self.lines.copy()
        for ind,t in enumerate(self.lines):
            t = t.replace("\x1b",' ')
            t = t.split(" ")
            
            indices = np.where(np.array(t) == '[0m')[0]

            for i in indices:
                temp = t[i]
                t[i] = t[i-2]
                t[i-2] = temp

            flipped_lines[ind] = ''.join(["\x1b"+c if c.startswith('[') else " "+c for c in t[::-1]] )
        return sprite(lines = flipped_lines,spacing=self.spacing)


    def join(self, sprite2, spacing):
        """
        Function that puts 2 sprites next to each other.

        :param sprite2: Sprite to put ont the right of current sprite
        :param spacing: Spacing in between sprites
        :return: Joined sprites as one Sprite
        """
        sprite1_lines = self.lines
        sprite2_lines = sprite2.lines
        len1 = len(sprite1_lines)
        len2 = len(sprite2_lines)

        # Add empty lines above shorter sprite (so sprites are on same level)
        if len1 > len2:
            lines_to_add = (len1-len2)
            sprite2_lines = [" " * (sprite2.width)] * lines_to_add + sprite2_lines
        elif len2 > len1:
            lines_to_add = (len2-len1)
            sprite1_lines = [" " * (self.width)] * lines_to_add + sprite1_lines

        joined_lines = [sprite1_lines[i] + " "*spacing + sprite2_lines[i] for i in range(len(sprite1_lines))]
        joined_sprite = sprite(lines=joined_lines)
        return(joined_sprite)
            
    
    def show(self):
        """Function that shows current sprite."""
        print(self.text)
