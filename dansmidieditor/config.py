from controls import Controls, Mode
from editor import Editor

import re
import traceback

"""
configuration='''
mode .*
order -200
.* q: self.command('quit')
.* <Backspace >Backspace:
 if self.mode=='command':
  i=0
  for i in reversed(range(len(self.sequence)-2)):
   if self.sequence[i][0]=='<': break
  self.sequence=self.sequence[:i]
 elif self.mode in ['insert', 'normal'] and len(self.sequence)==2:
  note=self.view.remove_note(self.view.previous_note())
  if note: self.view.cursor.coincide_note(note)
  self.sequence=self.sequence[:-2]
 else: self.sequence=self.sequence[:-3]
end
.* x.*: self.sequence=self.sequence[:-1]
 <Esc >Esc: self.reset()
.* <LShift >LShift: self.sequence=self.sequence[:-2]; self.shift=False
.* <RShift >RShift: self.sequence=self.sequence[:-2]; self.shift=False
.* <.Shift$: self.shift=True
.+ >.Shift$: self.shift=False
 >.Shift$: self.shift=False; self.clear()
order -100
.* >Esc: self.clear()
order 100
 >: self.clear()

mode normal
order -300
 <Esc >Esc:
 self.view.cancel_visual() or self.view.deselect()
 self.clear()
order 0
.* >j:
 if self.shift:       self.view.cursor_note_down  (self.reps())
 else:                self.view.cursor_down       (self.reps())
 self.clear()
.* >k:
 if self.shift:       self.view.cursor_note_up    (self.reps())
 else:                self.view.cursor_up         (self.reps())
 self.clear()
.* >l:                self.view.cursor_right      (self.reps());                   self.clear()
.* >h:                self.view.cursor_left       (self.reps());                   self.clear()
 <i >i$:              self.mode='insert';                                          self.clear()
 <Return >Return:     self.view.select();                                          self.clear()
 <Delete >Delete:     self.view.delete();                                          self.clear()
.* >s:                self.view.more_multistaffing(self.reps());                   self.clear()
.* >x:                self.view.less_multistaffing(self.reps());                   self.clear()
 <.Shift <;$:         self.mode='command';                                         self.clear()
.* >v:                self.view.toggle_visual();                                   self.clear()
.* >y:                self.view.yank(); self.view.deselect();                      self.clear()
.* >p:                self.view.put();                                             self.clear()
 <.Shift <i$:         self.view.info();                                            self.clear()
 <PageUp >PageUp:     self.view.transpose_notes(self.view.selected,  12);          self.clear()
 <PageDown >PageDown: self.view.transpose_notes(self.view.selected, -12);          self.clear()
 <z >z:               self.view.duration+=360*4;                                   self.clear()
 <c >c:               self.view.duration=max(360*4, self.view.duration-360*4);     self.clear()
 <a <z >z:            self.view.harmonize(self.view.selected, 12);                 self.clear()
 <a <s >s:            self.view.harmonize(self.view.selected,  1);                 self.clear()
 <a <x >x:            self.view.harmonize(self.view.selected,  2);                 self.clear()
 <a <d >d:            self.view.harmonize(self.view.selected,  3);                 self.clear()
 <a <c >c:            self.view.harmonize(self.view.selected,  4);                 self.clear()
 <a <v >v:            self.view.harmonize(self.view.selected,  5);                 self.clear()
 <a <g >g:            self.view.harmonize(self.view.selected,  6);                 self.clear()
 <a <b >b:            self.view.harmonize(self.view.selected,  7);                 self.clear()
 <a <h >h:            self.view.harmonize(self.view.selected,  8);                 self.clear()
 <a <n >n:            self.view.harmonize(self.view.selected,  9);                 self.clear()
 <a <j >j:            self.view.harmonize(self.view.selected, 10);                 self.clear()
 <a <m >m:            self.view.harmonize(self.view.selected, 11);                 self.clear()

mode command
 .*>Return: self.command()

mode insert
 (<.Shift )?<z >z:    self.view.add_note( 0, not self.shift);                      self.clear()
 (<.Shift )?<s >s:    self.view.add_note( 1, not self.shift);                      self.clear()
 (<.Shift )?<x >x:    self.view.add_note( 2, not self.shift);                      self.clear()
 (<.Shift )?<d >d:    self.view.add_note( 3, not self.shift);                      self.clear()
 (<.Shift )?<c >c:    self.view.add_note( 4, not self.shift);                      self.clear()
 (<.Shift )?<v >v:    self.view.add_note( 5, not self.shift);                      self.clear()
 (<.Shift )?<g >g:    self.view.add_note( 6, not self.shift);                      self.clear()
 (<.Shift )?<b >b:    self.view.add_note( 7, not self.shift);                      self.clear()
 (<.Shift )?<h >h:    self.view.add_note( 8, not self.shift);                      self.clear()
 (<.Shift )?<n >n:    self.view.add_note( 9, not self.shift);                      self.clear()
 (<.Shift )?<j >j:    self.view.add_note(10, not self.shift);                      self.clear()
 (<.Shift )?<m >m:    self.view.add_note(11, not self.shift);                      self.clear()
 <Space >Space:       self.view.cursor_right();                                    self.clear()
 <PageUp >PageUp:     self.view.transpose_notes([self.view.previous_note()],  12); self.clear()
 <PageDown >PageDown: self.view.transpose_notes([self.view.previous_note()], -12); self.clear()

mode (insert|normal)
.* >d:
 if self.view.selected: self.view.durate(self.fraction())
 else: self.view.set_duration(self.fraction())
 self.clear()
'''

class Mode:
	def __init__(self):
		#self.configure(configuration)
		self.done=False
		#self.view=View()
		self.shift=False
		self.command_aliases={
			'q': 'quit',
			'e': 'edit',
			'w': 'write',
			'h': 'help',
			'von': 'vel_on',
			'vel_down': 'vel_on',
			'vd': 'vel_on',
		}
		self.messaging=False

	def reps(self):
		try: return int(re.match(r'\d+', self.sequence_as_text()).group())
		except: return 1

	def fraction(self, skip=0):
		from fractions import Fraction
		try:
			s=self.sequence_as_text()[skip:]
			m=re.search('([0-9]+)/([0-9]+)', s)
			if m: return Fraction(*[int(i) for i in m.groups()])
			return Fraction(int(s[:-1]), 1)
		except: return Fraction(1)

	def command(self, command=None):
		if not command: command=self.sequence_as_text()
		command=command.split()
		if not command: self.reset(); return
		name=command[0]
		self.force=False
		if name.endswith('!'): self.force=True; name=name[:-1]
		name=self.command_aliases.get(name, name)
		command_name='command_'+name
		params=command[1:]
		if hasattr(self, command_name):
			try:
				result=getattr(self, command_name)(*params)
				if type(result)==str: self.message(result)
				else: self.reset()
			except:
				traceback.print_exc()
				self.message('error!')
		else: self.message('no such command "{}"'.format(name))

	def check_unwritten(self):
		if self.view.unwritten and not self.force:
			self.message('unwritten changes, use q! to force quit')
			return False
		return True

	def message(self, message):
		self.reset()
		self.view.text=message
		self.messaging=True

	#commands
	def command_quit(self):
		if self.check_unwritten(): self.done=True
	def command_edit(self, path):
		if self.check_unwritten(): self.view.read(path)
	def command_load(self, path):
		if self.check_unwritten(): self.view.read(path, remember=False)
	def command_write(self, *args): self.view.write(*args)
	def command_wq(self, *args): self.command_write(*args); self.command_quit()
	def command_pdb(self): import pdb; pdb.set_trace()
	def command_help(self, *args):
		if len(args)==0:
			print('help with what?')
			print('configuration')
			print('command')
		elif len(args)==1:
			if args[0]=='configuration': print('configuration:\n'+configuration)
			elif args[0]=='command':
				print('commands:')
				for i in dir(self):
					if callable(getattr(self, i)) and i.startswith('command_'): print(i[8:])
			else: print('no such help topic "{}"'.format(args[0]))
		return 'see terminal for details'
	def command_tempo(self, quarters_per_minute): self.view.add_tempo(float(quarters_per_minute))
	def command_track(self): self.view.midi.append([])
	def command_quantize(self, divisor=None):
		if divisor is None: divisor=self.view.ticks_per_quarter()/self.view.cursor.duration
		self.view.quantize(int(divisor))
	def command_vel_on(self, vel):
		self.view.set_vel(int(vel))

	#callback
	def on_input(self):
		if self.messaging: self.messaging=False; return
		if   self.mode=='command': self.view.text=':'+self.sequence_as_text()
		elif self.mode=='insert' : self.view.text='i'+''.join(self.sequence)
		else                     : self.view.text=    ''.join(self.sequence)
"""

class EditorMode(Mode):
    def __init__(self, editor):
        self.editor = editor

class NormalMode(EditorMode):
    def enter(self, controls):
        self.controls = controls
        controls.clear()
        controls.set_channel('immediate')
        self.reps = None

    def handle_input(self, controls):
        direction, key, modifiers = controls.input
        if direction == '+':
            if '0' <= key <= '9':
                if not self.reps: self.reps = 0
                self.reps = self.reps * 10 + int(key)
            else:
                action = {
                    'h': lambda: self.editor.cursor_left(self.take_reps()),
                    'j': lambda: self.editor.cursor_down(self.take_reps()),
                    'k': lambda: self.editor.cursor_up(self.take_reps()),
                    'l': lambda: self.editor.cursor_right(self.take_reps()),
                    'J': lambda: self.editor.cursor_note_down(self.take_reps()),
                    'K': lambda: self.editor.cursor_note_up(self.take_reps()),
                    ':': lambda: controls.set_mode('command'),
                    'escape': lambda: self.take_reps(),
                    'backspace': lambda: self.remove_reps_digit(),
                }.get(key)
                if action: action()
        if not isinstance(controls.mode, NormalMode): return
        text_segments = []
        if self.reps:
            text_segments.append(str(self.reps))
        text_segments.append(controls.status())
        self.editor.text = ' '.join(text_segments)

    def take_reps(self):
        if self.reps:
            r = self.reps
            self.reps = None
            return r
        else:
            return 1

    def remove_reps_digit(self):
        if not self.reps: return
        self.reps //= 10
        if self.reps == 0: self.reps = None

class CommandMode(EditorMode):
    def enter(self, controls):
        self.controls = controls
        controls.clear()
        controls.set_channel('text')
        self.editor.text = ':'

    def handle_input(self, controls):
        direction, key, modifiers = controls.input
        if direction == '+':
            if key == 'escape':
                controls.set_mode('normal')
            elif key == 'enter':
                if controls.status() == 'q':
                    self.command_quit()
            else:
                self.editor.text = f':{controls.status()}'

    # helpers
    def check_unwritten(self):
        if self.editor.unwritten:
            self.message('unwritten changes, use q! to force quit')
            return False
        return True

    # commands
    def command_quit(self):
        if self.check_unwritten():
            self.controls.udata['done'] = True

def configure(editor):
    controls = Controls(
        'normal',
        normal=NormalMode(editor),
        command=CommandMode(editor),
    )
    controls.udata['done'] = False
    return controls
