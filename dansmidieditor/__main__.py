#!/usr/bin/env python3

#===== imports =====#
#----- project -----#
from config import configure
from editor import Editor

#----- 3rd party -----#
import pyglet

#----- standard -----#
import sys

#===== init =====#
editor = Editor()
controls = configure(editor)

#===== args =====#
for arg in sys.argv[1:]:
    controls.set_mode('command')
    controls.handle_text(arg)
    controls.set_mode('normal')

if controls.udata['done']:
    sys.exit()

#===== helpers =====#
def symbol_to_key(symbol):
    return symbol_to_key.d.get(symbol)

symbol_to_key.d = {
    # alphabet
    pyglet.window.key.A: 'a',
    pyglet.window.key.B: 'b',
    pyglet.window.key.C: 'c',
    pyglet.window.key.D: 'd',
    pyglet.window.key.E: 'e',
    pyglet.window.key.F: 'f',
    pyglet.window.key.G: 'g',
    pyglet.window.key.H: 'h',
    pyglet.window.key.I: 'i',
    pyglet.window.key.J: 'j',
    pyglet.window.key.K: 'k',
    pyglet.window.key.L: 'l',
    pyglet.window.key.M: 'm',
    pyglet.window.key.N: 'n',
    pyglet.window.key.O: 'o',
    pyglet.window.key.P: 'p',
    pyglet.window.key.Q: 'q',
    pyglet.window.key.R: 'r',
    pyglet.window.key.S: 's',
    pyglet.window.key.T: 't',
    pyglet.window.key.U: 'u',
    pyglet.window.key.V: 'v',
    pyglet.window.key.W: 'w',
    pyglet.window.key.X: 'x',
    pyglet.window.key.Y: 'y',
    pyglet.window.key.Z: 'z',
    # regular numbers
    pyglet.window.key._0: '0',
    pyglet.window.key._1: '1',
    pyglet.window.key._2: '2',
    pyglet.window.key._3: '3',
    pyglet.window.key._4: '4',
    pyglet.window.key._5: '5',
    pyglet.window.key._6: '6',
    pyglet.window.key._7: '7',
    pyglet.window.key._8: '8',
    pyglet.window.key._9: '9',
    pyglet.window.key._0: '0',
    # special characters
    pyglet.window.key.QUOTELEFT: '`',
    pyglet.window.key.MINUS: '-',
    pyglet.window.key.EQUAL: '=',
    pyglet.window.key.BRACKETLEFT: '[',
    pyglet.window.key.BRACKETRIGHT: ']',
    pyglet.window.key.BACKSLASH: '\\',
    pyglet.window.key.SEMICOLON: ';',
    pyglet.window.key.APOSTROPHE: "'",
    pyglet.window.key.COMMA: ',',
    pyglet.window.key.PERIOD: '.',
    pyglet.window.key.SLASH: '/',
    pyglet.window.key.SPACE: ' ',
    pyglet.window.key.ASCIITILDE: '~',
    pyglet.window.key.EXCLAMATION: '!',
    pyglet.window.key.AT: '@',
    pyglet.window.key.HASH: '#',
    pyglet.window.key.DOLLAR: '$',
    pyglet.window.key.PERCENT: '%',
    pyglet.window.key.ASCIICIRCUM: '^',
    pyglet.window.key.AMPERSAND: '&',
    pyglet.window.key.ASTERISK: '*',
    pyglet.window.key.PARENLEFT: '(',
    pyglet.window.key.PARENRIGHT: ')',
    pyglet.window.key.UNDERSCORE: '_',
    pyglet.window.key.PLUS : '+',
    pyglet.window.key.BRACELEFT: '{',
    pyglet.window.key.BRACERIGHT: '}',
    pyglet.window.key.BAR: '|',
    pyglet.window.key.COLON: ':',
    pyglet.window.key.DOUBLEQUOTE: '"',
    pyglet.window.key.LESS: '<',
    pyglet.window.key.GREATER: '>',
    pyglet.window.key.QUESTION: '?',
    # modifiers
    pyglet.window.key.LSHIFT: 'l_shift',
    pyglet.window.key.RSHIFT: 'r_shift',
    pyglet.window.key.LCTRL: 'l_ctrl',
    pyglet.window.key.RCTRL: 'r_ctrl',
    pyglet.window.key.LALT: 'l_alt',
    pyglet.window.key.RALT: 'r_alt',
    pyglet.window.key.LOPTION: 'l_option',
    pyglet.window.key.ROPTION: 'r_option',
    # control
    pyglet.window.key.ESCAPE: 'escape',
    pyglet.window.key.BACKSPACE: 'backspace',
    pyglet.window.key.TAB: 'tab',
    pyglet.window.key.ENTER: 'enter',
    pyglet.window.key.INSERT: 'insert',
    pyglet.window.key.HOME: 'home',
    pyglet.window.key.PAGEUP: 'page_up',
    pyglet.window.key.DELETE: 'delete',
    pyglet.window.key.END: 'end',
    pyglet.window.key.PAGEDOWN: 'page_down',
    pyglet.window.key.UP: 'up',
    pyglet.window.key.LEFT: 'left',
    pyglet.window.key.DOWN: 'down',
    pyglet.window.key.RIGHT: 'right',
    # function
    pyglet.window.key.F1: 'f1',
    pyglet.window.key.F2: 'f2',
    pyglet.window.key.F3: 'f3',
    pyglet.window.key.F4: 'f4',
    pyglet.window.key.F5: 'f5',
    pyglet.window.key.F6: 'f6',
    pyglet.window.key.F7: 'f7',
    pyglet.window.key.F8: 'f8',
    pyglet.window.key.F9: 'f9',
    pyglet.window.key.F10: 'f10',
    pyglet.window.key.F11: 'f11',
    pyglet.window.key.F12: 'f12',
    # numpad
    pyglet.window.key.NUM_0: '0',
    pyglet.window.key.NUM_1: '1',
    pyglet.window.key.NUM_2: '2',
    pyglet.window.key.NUM_3: '3',
    pyglet.window.key.NUM_4: '4',
    pyglet.window.key.NUM_5: '5',
    pyglet.window.key.NUM_6: '6',
    pyglet.window.key.NUM_7: '7',
    pyglet.window.key.NUM_8: '8',
    pyglet.window.key.NUM_9: '9',
    pyglet.window.key.NUM_DIVIDE: '/',
    pyglet.window.key.NUM_MULTIPLY: '*',
    pyglet.window.key.NUM_SUBTRACT: '-',
    pyglet.window.key.NUM_ADD: '+',
    pyglet.window.key.NUM_ENTER: 'enter',
    pyglet.window.key.NUM_DECIMAL: '.',
    pyglet.window.key.NUM_HOME: 'home',
    pyglet.window.key.NUM_UP: 'up',
    pyglet.window.key.NUM_PAGE_UP: 'page_up',
    pyglet.window.key.NUM_LEFT: 'left',
    pyglet.window.key.NUM_RIGHT: 'right',
    pyglet.window.key.NUM_END: 'end',
    pyglet.window.key.NUM_DOWN: 'down',
    pyglet.window.key.NUM_PAGE_DOWN: 'page_down',
    pyglet.window.key.NUM_INSERT: 'insert',
    pyglet.window.key.NUM_DELETE: 'delete',
    pyglet.window.key.NUM_EQUAL: '=',
    pyglet.window.key.NUM_F1: 'f1',
    pyglet.window.key.NUM_F2: 'f2',
    pyglet.window.key.NUM_F3: 'f3',
    pyglet.window.key.NUM_F4: 'f4',
    pyglet.window.key.NUM_SPACE: ' ',
    pyglet.window.key.NUM_TAB: 'tab',
}

def translate_modifiers(pyglet_modifiers):
    modifiers = set()
    if pyglet_modifiers & pyglet.window.key.MOD_SHIFT:
        modifiers.add('shift')
    if pyglet_modifiers & pyglet.window.key.MOD_CTRL:
        modifiers.add('ctrl')
    if pyglet_modifiers & (pyglet.window.key.MOD_ALT | pyglet.window.key.MOD_OPTION):
        modifiers.add('alt')
    return modifiers

#===== run =====#
window = pyglet.window.Window(caption="Dan's MIDI Editor", vsync=True, resizable=True)

@window.event
def on_key_press(symbol, modifiers):
    if key := symbol_to_key(symbol):
        if modifiers & pyglet.window.key.MOD_SHIFT and 'a' <= key <= 'z':
            key = key.upper()
        controls.handle_input(key, '+', translate_modifiers(modifiers))
        if controls.udata['done']:
            window.close()
    return pyglet.event.EVENT_HANDLED

@window.event
def on_key_release(symbol, modifiers):
    if key := symbol_to_key(symbol):
        controls.handle_input(key, '-', translate_modifiers(modifiers))
        if controls.udata['done']:
            window.close()
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    editor.draw(window)

pyglet.app.run()
