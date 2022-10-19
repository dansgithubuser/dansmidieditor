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
    controls.udata['command'](arg)

if controls.udata['done']:
    sys.exit()

#===== helpers =====#
def symbol_to_key(symbol):
    {
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
        pyglet.window.key.MINUS: '-',
        pyglet.window.key.EQUAL: '=',
        pyglet.window.key.BACKSLASH: '\\',
        pyglet.window.key.ENTER: 'enter',
        pyglet.window.key.SPACE: 'space',
        pyglet.window.key.BACKSPACE: 'backspace',
        pyglet.window.key.DELETE: 'delete',
        pyglet.window.key.LEFT: 'left',
        pyglet.window.key.RIGHT: 'right',
        pyglet.window.key.UP: 'up',
        pyglet.window.key.DOWN: 'down',
        pyglet.window.key.HOME: 'home',
        pyglet.window.key.END: 'end',
        pyglet.window.key.PAGEUP: 'page_up',
        pyglet.window.key.PAGEDOWN: 'page_down',
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
        pyglet.window.key.NUM_EQUAL: '=',
        pyglet.window.key.NUM_DIVIDE: '/',
        pyglet.window.key.NUM_MULTIPLY: '*',
        pyglet.window.key.NUM_SUBTRACT: '-',
        pyglet.window.key.NUM_ADD: '+',
        pyglet.window.key.NUM_DECIMAL: '.',
        pyglet.window.key.NUM_ENTER: 'enter',
    }.get(symbol)

def translate_modifiers(pyglet_modifiers):
    modifiers = set()
    if pyglet_modifiers & pyglet.MOD_SHIFT:
        modifiers.add('shift')
    if pyglet_modifiers & pyglet.MOD_CTRL:
        modifiers.add('ctrl')
    if pyglet_modifiers & (pyglet.MOD_ALT | pyglet.MOD_OPTION):
        modifiers.add('alt')

#===== run =====#
window = pyglet.window.Window(caption="Dan's MIDI Editor", vsync=True, resizable=True)

@window.event
def on_key_press(symbol, modifiers):
    if key := symbol_to_key(symbol):
        controls.handle_input(key, '+', translate_modifiers(modifiers))
        if controls.udata['done']:
            window.close()

@window.event
def on_key_release(symbol, modifiers):
    if key := symbol_to_key(symbol):
        controls.handle_input(key, '-', translate_modifiers(modifiers))
        if controls.udata['done']:
            window.close()

@window.event
def on_draw():
    editor.draw(window)

pyglet.app.run()
