class dialogbox:
    """Class for creating and displaying an ANSI escape code based dialogbox"""
    def __init__(self, edge_color = [0,0,0], bg_color = [254,254,254], text_color = [0,0,0], border=0, spacing=0, text_centered=True):
        """
        Creates a dialogbox.

        :param edge_color: RGB Color of the edge of the dialogbox ([0,0,0])
        :param bg_color: RGB Color of the background of the dialogbox ([254,254,254])
        :param text_color: RGB Color of the dialogbox texg ([0,0,0])
        :param border: Space from edge to text
        :param spacing: Space before dialogbox
        :param text_centered: bool for centering text
        """
        self.lines = None                            # Dialogbox text
        self.lines_col = text_color                  # Dialogbox text color
        self.edge_col = edge_color                  # Dialogbox edge color
        self.bg_col = bg_color                      # Dialogbox background color
        self.shdw_col = [c-45 for c in bg_color]    # Dialogbox shadow color (slightly darker than bg)
        self.border = border                        # Space from edge to text
        self.spacing = spacing                      # Spaces before dialogbox
        self.lines_centered = text_centered

    def center(self, width):
        """
        Function that centers the dialogbox in the frame.

        :param width: Width of frame
        """
        self.spacing = round((width - self.width)/2)
        self.render()

    def __call__(self, lines):
        """
        Function to convert text to ANSI dialogbox.

        :param lines: list of lines to add to dialogbox
        :return: ANSI dialogbox with text
        """
        self.lines = lines
        self.render()
        return (self.ansi)
        
    def position_text(self):
        """
        Function to position text in dialogbox based on centering bool.
        """
        positioned_lines = self.lines.copy()
        max_length = len(max(positioned_lines,key=len))   # Longest line in lines

        for i,t in enumerate(positioned_lines):
            length_diff = max_length-len(t)               # Length difference from longest line
            # Center
            if self.lines_centered:
                text_spacing = self.border + int((length_diff+(max_length % 2))/2)
                positioned_lines[i] = (' '*(text_spacing)) + t + (' '*((text_spacing) + len(t) % 2))
            # Don't center
            else:
                text_spacing = self.border + length_diff
                positioned_lines[i] = ' ' * self.border + t + ' '*text_spacing

        return positioned_lines

    def render(self):
        """Function to render dialogbox in ANSI format."""
        space = ' '                                 # Space
        new_line = '\n'+self.spacing*' '            # New line + spaces before dialogbox

        edge = ";".join(map(str,self.edge_col))     # Edge color as string to add to ANSI code
        bg = ";".join(map(str,self.bg_col))         # Bg color as string to add to ANSI code
        shdw = ";".join(map(str,self.shdw_col))     # Shadow color as string to add to ANSI code
        txt = ";".join(map(str,self.lines_col))     # Text color as string to add to ANSI code

        positioned_lines = self.position_text()
        max_length = len(max(positioned_lines,key=len))    # Longest string
        self.width = max_length + 6      # 2 edges of length 3
        # Textbox in ANSI format
        self.ansi =  (
            f'{self.spacing*space} \x1b[38;2;{edge}m▄\x1b[38;2;{shdw};48;2;{edge}m▄\x1b[38;2;{edge};48;2;{bg}m{"▀"*(max_length-4)}\x1b[38;2;{shdw};48;2;{edge}m▄\x1b[m\x1b[38;2;{edge}m▄ \x1b[m{new_line}' +
            f'\x1b[48;2;{edge}m \x1b[38;2;{bg};48;2;{shdw}m▄\x1b[48;2;{bg}m{space*(max_length-2)}\x1b[38;2;{bg};48;2;{shdw}m▄\x1b[m\x1b[48;2;{edge}m \x1b[m{new_line}' +
            f'\x1b[48;2;{edge}m \x1b[48;2;{bg}m{space*(max_length)}\x1b[m\x1b[48;2;{edge}m \x1b[m{new_line}'*int(self.border/2) +
            "".join(f'\x1b[48;2;{edge}m \x1b[48;2;{bg}m\x1b[38;2;{txt}m{t}\x1b[m\x1b[48;2;{edge}m \x1b[m{new_line}' for t in positioned_lines) +
            f'\x1b[48;2;{edge}m \x1b[48;2;{bg}m{space*(max_length)}\x1b[m\x1b[48;2;{edge}m \x1b[m{new_line}'*(int(self.border/2)) +
            f'\x1b[48;2;{edge}m \x1b[38;2;{bg};48;2;{shdw}m▀\x1b[48;2;{bg}m{space*(max_length-2)}\x1b[m\x1b[38;2;{bg};48;2;{shdw}m▀\x1b[48;2;{edge}m \x1b[m{new_line}' +
            f' \x1b[38;2;{edge}m▀\x1b[38;2;{edge};48;2;{shdw}m▄\x1b[38;2;{edge};48;2;{bg}m{"▄"*(max_length-4)}\x1b[m\x1b[38;2;{edge};48;2;{shdw}m▄\x1b[m\x1b[38;2;{edge}m▀\x1b[m'
        )
    
    def show(self):
        """Function to print ANSI dialogbox."""
        if self.lines != None:
            self.render()
            print(self.ansi)