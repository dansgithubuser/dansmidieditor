class Mode:
    def enter(self, controls): pass
    def exit(self, controls): pass
    def handle_input(self, controls): pass

class Controls:
    def __init__(self, mode_i, **modes):
        self.modes = modes
        self.mode = None
        self.key = None
        self.direction = None
        self.modifiers = None
        self.input = (None, None, None)
        self.channel = 'immediate'
        self.sequence = []
        self.text = []
        self.udata = {}
        self.set_mode(mode_i)

    def handle_input(self, direction, key, modifiers):
        self.direction = direction
        self.key = key
        self.modifiers = modifiers
        self.input = (direction, key, modifiers)
        if self.channel == 'sequence':
            self.sequence.append((direction, key, modifiers))
        elif self.channel == 'text':
            if direction == '+':
                if len(key) == 1:
                    self.text.append(key)
                elif key == 'backspace':
                    if self.text: self.text.pop()
        self.mode.handle_input(self)

    def handle_text(self, text, direction='+', key='enter', modifiers=set()):
        assert self.channel == 'text'
        self.text += text
        self.handle_input(direction, key, modifiers)

    def status(self):
        if self.channel == 'immediate':
            return ''
        elif self.channel == 'sequence':
            return ' '.join([i[0] + i[1] for i in self.sequence])
        elif self.channel == 'text':
            return ''.join(self.text)
        else:
            raise Exception(f'Unknown channel: {self.channel}')

    def set_channel(self, channel):
        if channel not in ['immediate', 'sequence', 'text']:
            raise Exception(f'Unknown channel: {self.channel}')
        self.channel = channel

    def set_mode(self, mode_name):
        if self.mode: self.mode.exit(self)
        self.mode = self.modes[mode_name]
        self.mode.enter(self)

    def clear(self):
        self.sequence.clear()
        self.text.clear()
