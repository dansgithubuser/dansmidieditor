from controls import AbstractControls
from view import View, midi
import re
import traceback

configuration='''
mode .*
order -1
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
order 0
.* >Esc: self.clear()
order 1
 >: self.clear()

mode normal
order -2
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
.* >Down:             self.view.transpose         (-self.reps());                  self.clear()
.* >Up:               self.view.transpose         ( self.reps());                  self.clear()
.* >Left:             self.view.translate         (-self.reps());                  self.clear()
.* >Right:            self.view.translate         ( self.reps());                  self.clear()
 <Delete >Delete:     self.view.delete();                                          self.clear()
.* >s: if self.shift: self.view.more_multistaffing(self.reps());                   self.clear()
.* >x: if self.shift: self.view.less_multistaffing(self.reps());                   self.clear()
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

class Controls(AbstractControls):
	def __init__(self):
		self.configure(configuration)
		AbstractControls.__init__(self)
		self.done=False
		self.view=View()
		self.shift=False
		self.command_aliases={
			'q': 'quit',
			'e': 'edit',
			'w': 'write',
			'h': 'help',
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
		midi.quantize(self.view.midi, int(divisor))

	#callback
	def on_input(self):
		if self.messaging: self.messaging=False; return
		if   self.mode=='command': self.view.text=':'+self.sequence_as_text()
		elif self.mode=='insert' : self.view.text='i'+''.join(self.sequence)
		else                     : self.view.text=    ''.join(self.sequence)

controls=Controls()
