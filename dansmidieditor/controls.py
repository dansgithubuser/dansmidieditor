class Controls:
    def __init__(self, mode):
        self.mode = mode
        self.key = None
        self.direction = None
        self.modifiers = None
        self.channel = 'sequence'
        self.sequence = []
        self.text = []
        self.udata = {}
        self.shift_table = {
            'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F',
            'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L',
            'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R',
            's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X',
            'y': 'Y', 'z': 'Z',
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
            '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '[': '{', ']': '}', ';': ':', ',': '<', '.': '>',
            "'": '"', '/': '?', '`': '~', '=': '+', '-': '_',
            '\\': '|',
        }

    def handle_input(self, key, direction, modifiers):
        self.key = key
        self.direction = direction
        self.modifiers = modifiers
        if self.channel == 'sequence':
            self.sequence.append(direction + key)
        elif self.channel == 'text':
            if key in self.shift_table:
                if modifiers['shift']:
                    self.text.append(self.shift_table[key])
                else:
                    self.text.append(key)
            elif key == 'space':
                self.text.append(' ')
            elif key == 'backspace':
                self.text.pop()
        else:
            raise Exception(f'Unknown channel: {self.channel}')
        self.mode.handle_input(self)

    def status(self):
        if self.channel == 'sequence':
            return ' '.join(self.sequence)
        elif self.channel == 'text':
            return ''.join(self.text)
        else:
            raise Exception(f'Unknown channel: {self.channel}')

    def set_channel(self, channel):
        if channel not in ['sequence', 'text']:
            raise Exception(f'Unknown channel: {self.channel}')
        self.channel = channel
