import copy
from fractions import Fraction
import os
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'deps',
        'dansmidilibs',
    )
)
import midi

us_per_minute = 60e6
tonics = [
    'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F',
    'C',
    'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#',
]

class Cursor:
    def __init__(self, ticks_per_quarter):
        self.staff = 0
        self.note = 60
        self.ticks = Fraction(0)
        self.duration = Fraction(ticks_per_quarter)
        self.duty = Fraction(1)

    def end(self):
        return self.ticks + self.duration

    def coincide_note(self, note):
        self.ticks = Fraction(note.ticks)
        self.duration = Fraction(note.duration())

class Batch:
    def __init__(self, pyglet, h_window):
        self.pyglet = pyglet
        self.h_window = h_window
        self.batch = None
        self.list = []
        self.reset()

    def add_fill(self, xi, yi, xf=None, yf=None, w=None, h=None, color=(1, 1, 1, 1)):
        if w:
            xf = xi + w
        if h:
            yf = yi + h
        yi = self.h_window - yi
        yf = self.h_window - yf
        rectangle = self.pyglet.shapes.Rectangle(
            xi,
            yi,
            xf-xi,
            yf-yi,
            color=tuple(int(255*i) for i in color[:3]),
            batch=self.batch,
        )
        rectangle.opacity = int(color[3] * 255)
        self.list.append(rectangle)

    def add_text(self, s, x, y, h, color, anchor_x='left', anchor_y='baseline'):
        y = self.h_window - y
        label = self.pyglet.text.Label(
            s,
            font_name='Courier New',
            font_size=h,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=tuple(int(255*i) for i in color),
            batch=self.batch,
        )
        self.list.append(label)

    def draw(self, reset):
        self.batch.draw()
        if reset:
            self.reset()

    def reset(self):
        self.batch = self.pyglet.graphics.Batch()
        self.list.clear()

class Editor:
    'We use track 0 for messages that affect all staves, such as tempo. We ensure this track always exists.'

    def __init__(self, pyglet):
        self.song = midi.Song()
        self.text = ''
        self.staff = 0
        self.staves = 4.0
        self.multistaffing = 1
        self.ticks = 0
        self.duration = 5760
        self.cursor = Cursor(self.song.ticks_per_quarter)
        self.deselect()
        self.unyank()
        self.visual = Cursor(0)
        self.visual.active = False
        self.unwritten = False
        self.path = 'untitled.mid'
        self.pyglet = pyglet
        # layout
        self.margin = 6  # distance stuff should be from edge of screen, if it shouldn't touch
        self.text_size = 10
        self.banner_h = self.margin + self.text_size * 4  # space at top for track 0 messages
        self.footer_h = self.margin + self.text_size * 2  # space at bottom for text
        # colors
        self.color_background = [   0,    0,    0,    1]
        self.color_staves     = [   0,  1/4,    0,  1/2]
        self.color_c_line     = [ 1/4,  1/4,  1/4,  1/2]
        self.color_quarter    = [1/16, 1/16, 1/16,    1]
        self.color_notes      = [   0,  1/2,  1/2,    1]
        self.color_octaves    = [ 3/4,  3/4,  3/4,    1]
        self.color_other      = [   0,    1,    0,    1]
        self.color_cursor     = [ 1/2,    0,  1/2,  1/2]
        self.color_visual     = [   1,    1,    1,  1/4]
        self.color_selected   = [   1,    1,    1,    1]
        self.color_warning    = [   1,    0,    0,    1]
        self.color_text       = [   1,    1,    1,    1]

    # persistence
    def read(self, path, remember=True):
        self.song.load(path)
        if not self.song.tracks: self.song.tracks.append(midi.Track())
        self.cursor.duration = Fraction(self.song.ticks_per_quarter)
        self.cursor_down(0)
        self.unwritten = False
        if remember: self.path = path

    def write(self, path=None):
        if not path: path = self.path
        self.song.save(path)
        self.unwritten = False

    # cursor
    def cursor_down(self, amount=1):
        self.cursor.staff += amount
        self.cursor.staff = max(self.cursor.staff, 0)
        self.cursor.staff = min(self.cursor.staff, len(self.song) - 2)
        # move up if cursor is above window
        self.staff = min(self.staff, self.cursor.staff)
        # move down if cursor is below window
        bottom = self.staff + int(self.staves) - 1
        if self.cursor.staff > bottom: self.staff += self.cursor.staff - bottom
        # figure cursor octave
        self.cursor.note %= 12
        self.cursor.note += self.calculate_octave(self.cursor.staff) * 12

    def cursor_up(self, amount=1): self.cursor_down(-amount)

    def cursor_right(self, amount=1):
        self.cursor.ticks += self.cursor.duration*amount
        self.cursor.ticks = max(Fraction(0), self.cursor.ticks)
        # move left if cursor is left of window
        self.ticks = min(self.ticks, int(self.cursor.ticks))
        # move right if cursor is right of window
        right = self.ticks + self.duration
        cursor_right = self.cursor.ticks + self.cursor.duration
        if cursor_right > right: self.ticks += int(cursor_right) - right

    def cursor_left(self, amount=1): self.cursor_right(-amount)

    def cursor_note_down(self, amount=1):
        self.cursor.note -= amount
        self.cursor.note = max(0, self.cursor.note)
        self.cursor.note = min(127, self.cursor.note)

    def cursor_note_up(self, amount=1): self.cursor_note_down(-amount)

    def set_duration(self, fraction_of_quarter):
        self.cursor.duration = Fraction(self.song.ticks_per_quarter) * fraction_of_quarter

    # window
    def more_multistaffing(self, amount=1):
        self.multistaffing += amount
        self.multistaffing = max(1, self.multistaffing)
        self.multistaffing = min(6, self.multistaffing)

    def less_multistaffing(self, amount=1): self.more_multistaffing(-amount)

    # notes
    def add_note(self, number, advance=True):
        octave = None
        for i in self.song[self.cursor.staff]:
            if i.type() != 'note': continue
            if i.ticks > self.ticks: break
            octave = i.number() // 12
        if octave is None: octave = self.calculate_octave(self.cursor.staff)
        self.song.add_note(
            self.cursor.staff + 1,
            int(self.cursor.ticks),
            int(self.cursor.duration*self.cursor.duty),
            number + 12 * octave,
        )
        if advance: self.cursor_right()
        self.unwritten = True

    def prev_note(self):
        return self.song.prev(self.cursor.staff + 1, int(self.cursor.ticks), predicate=Msg.is_note_start)

    def remove_note(self, ref):
        if ref == None: return
        return ref.remove()

    def transpose_notes(self, refs, semitones):
        for ref in refs:
            ref().transpose(semitones)

    def harmonize_notes(self, refs, semitones):
        for ref in refs: ref.denorm()
        for ref in refs:
            self.song.add_note(
                ref.track,
                ref().ticks,
                ref().duration(),
                ref().number() + semitones,
                ref().channel(),
            )
        for ref in refs: ref.renorm()

    # other midi events
    def add_tempo(self, quarters_per_minute):
        us_per_quarter = us_per_minute/quarters_per_minute
        self.song[0].add(
            midi.Msg.tempo(int(us_per_quarter)),
            int(self.cursor.ticks),
        )

    # selection
    def select(self):
        if self.visual.active: self.toggle_visual(); return
        kwargs = {
            'track_i': self.cursor.staff + 1,
            'track_f': self.cursor.staff + 1,
            'ticks_i': self.cursor.ticks,
            'ticks_f': self.cursor.end(),
        }
        notes = self.song.select(**kwargs, note_i=self.cursor.note, types=['note_on'])
        if not notes: notes = self.song.select(**kwargs, types=['note_on'])
        for i in notes: self.selected.add(i)

    def deselect(self): self.selected = set()

    def is_selected(self, note):
        for i in self.selected:
            if i() is note: return True
        return False

    def delete(self):
        self.yank()
        for i in self.selected: i.remove()
        self.selected = set()
        self.unwritten = True

    def transpose(self, semitones):
        for i in self.selected:
            i().transpose(semitones)
        self.unwritten = True

    def durate(self, cursor_durations):
        for i in self.selected:
            i().durate(int(self.cursor.duration * cursor_durations))
        self.unwritten = True

    def set_vel(self, vel):
        for i in self.selected:
            i().set_vel(vel)
        self.unwritten = True

    def get_visual_duration(self):
        ticks = sorted([
            self.visual.ticks, self.visual.ticks + self.visual.duration,
            self.cursor.ticks, self.cursor.ticks + self.cursor.duration,
        ])
        return ticks[0], ticks[-1]

    def toggle_visual(self):
        if self.visual.active:
            start, finish = self.get_visual_duration()
            notes = self.song.select(
                track_i=min(self.visual.staff, self.cursor.staff) + 1,
                track_f=max(self.visual.staff, self.cursor.staff) + 1,
                ticks_i=start,
                ticks_f=finish,
            )
            for i in notes: self.selected.add(i)
            self.visual.duration = finish - start
            self.visual.active = False
        else:
            self.visual = copy.deepcopy(self.cursor)
            self.visual.active = True

    def cancel_visual(self):
        if not self.visual.active: return False
        self.visual.active = False
        return True

    def yank(self):
        if self.visual.active: self.toggle_visual()
        self.yanked = [copy.deepcopy(i.denorm()) for i in self.selected]

    def unyank(self): self.yanked = []

    def put(self):
        if not self.yanked: return
        ticks_i = min([i().ticks for i in self.yanked])
        track_i = min([i.track for i in self.yanked])
        for i in self.yanked:
            self.song.add_note(
                self.cursor.staff + 1 + i.track - track_i,
                int(self.cursor.ticks - ticks_i + i().ticks),
                i().duration(),
                i().note(),
                i().channel(),
                i().vel(),
                i().vel_off(),
            )
        self.cursor.ticks += self.visual.duration

    def info(self):
        for i in sorted(self.selected, key=lambda x: (x.track, x.index)):
            print(self.song[i.track][i.index])

    # drawing
    def staves_to_draw(self):
        return range(
            self.staff,
            self.staff + min(
                int(self.staves) + 1,
                len(self.song) - 1 - self.staff,
            ),
        )

    def notes_per_staff(self):
        return 24 * self.multistaffing

    def h_staves(self):
        return self.h_window - self.banner_h - self.footer_h

    def h_note(self):
        return self.h_staves() // self.staves // self.notes_per_staff()

    def y_note(self, staff, note, octave=0):
        y_staff = (staff + 1 - self.staff) * self.h_staves() // self.staves
        return int(self.banner_h + y_staff - (note + 1 - 12 * octave) * self.h_note())

    def x_ticks(self, ticks):
        return (ticks - self.ticks) * self.w_window // self.duration

    def calculate_octave(self, staff):
        octave = 5
        lo = 60
        hi = 60
        for i in self.song[1 + staff]:
            if not i.is_note_start(): continue
            if i.note_end().ticks < self.ticks: continue
            if i.ticks >= self.ticks + self.duration: break
            lo = min(lo, i.note())
            hi = max(hi, i.note())
        top = (octave + 2) * 12
        if hi > top: octave += (hi - top + 11) // 12
        bottom = octave * 12
        if lo < bottom: octave += (lo - bottom) // 12
        return octave

    def notate_octave(self, octave):
        octave -= 5
        if octave >=  1: return '{}va'.format(1 + 7 * octave)
        if octave <= -1: return '{}vb'.format(1 - 7 * octave)
        return '.'

    def draw(self, window):
        pyglet = self.pyglet
        pyglet.gl.glClearColor(*self.color_background)
        window.clear()
        self.w_window, self.h_window = window.get_size()
        batch = Batch(pyglet, self.h_window)
        # quarters
        tph = 2 * self.song.ticks_per_quarter
        for i in range(self.duration // tph + 2):
            batch.add_fill(
                xi=self.x_ticks((self.ticks // tph + i) * tph),
                xf=self.x_ticks((self.ticks // tph + i) * tph + self.song.ticks_per_quarter),
                yi=0,
                yf=self.h_window,
                color=self.color_quarter
            )
        # staves
        h=int(self.h_note())
        for m in range(self.multistaffing):
            for i in self.staves_to_draw():
                batch.add_fill(
                    xi=0,
                    xf=self.w_window,
                    yi=self.y_note(i, 24*m),
                    h=h,
                    color=self.color_c_line,
                )
                for j in [4, 7, 11, 14, 17]:
                    batch.add_fill(
                        xi=0,
                        xf=self.w_window,
                        yi=self.y_note(i, j+24*m),
                        h=h,
                        color=self.color_staves,
                    )
        # octaves
        octaves = {}
        for staff in self.staves_to_draw():
            octaves[staff] = self.calculate_octave(staff)
            batch.add_text(
                self.notate_octave(octaves[staff]),
                x=self.margin,
                y=self.y_note(staff, 0) + self.h_note() / 2,
                h=self.text_size,
                color=self.color_octaves,
            )
        # tracks 1+
        for staff in self.staves_to_draw():
            track = self.song[1+staff]
            for deltamsg in track:
                if deltamsg.ticks >= self.ticks + self.duration: break
                if deltamsg.is_note_start():
                    if deltamsg.note_end().ticks < self.ticks: continue
                    kwargs={
                        'xi': self.x_ticks(deltamsg.ticks),
                        'xf': self.x_ticks(deltamsg.ticks + deltamsg.duration()),
                        'yi': self.y_note(staff, deltamsg.note(), octaves[staff]),
                    }
                    batch.add_fill(
                        h=int(self.h_note()),
                        color=self.color_selected if self.is_selected(deltamsg) else self.color_notes,
                        **kwargs,
                    )
                    if deltamsg.note() - 12 * octaves[staff] > 24 * self.multistaffing - 4:
                        batch.add_fill(
                            h=int(self.h_note() // 2),
                            color=self.color_warning,
                            **kwargs,
                        )
                else:
                    pass  # todo
        # track 0
        ticks = None
        line = 0
        for deltamsg in self.song[0]:
            if deltamsg.ticks < self.ticks: continue
            if deltamsg.ticks >= self.ticks + self.duration: break
            text = None
            if deltamsg.type() == 'tempo':
                text = f'q={us_per_minute // deltamsg.tempo_us_per_quarter()}'
            elif deltamsg.type() == 'time_sig':
                text = f'{deltamsg.time_sig_top()}/{deltamsg.time_sig_bottom()}'
            elif deltamsg.type() == 'key_sig':
                text = '{}{}'.format(
                    tonics[7 + deltamsg.key_sig_sharps() + (3 if deltamsg.key_sig_minor() else 0)],
                    '-' if deltamsg.key_sig_minor() else '+'
                )
            else:
                text = deltamsg.msg_str()
            if text:
                if ticks == None or deltamsg.ticks - ticks >= self.song.ticks_per_quarter:
                    line = 0
                else:
                    line += 1
                ticks = deltamsg.ticks
                batch.add_text(
                    text,
                    x=self.x_ticks(deltamsg.ticks),
                    y=self.margin + self.text_size * line,
                    anchor_y='top',
                    h=self.text_size,
                    color=self.color_other,
                )
        # cursor
        batch.add_fill(
            xi=self.x_ticks(int(self.cursor.ticks)),
            xf=self.x_ticks(int(self.cursor.ticks + self.cursor.duration)),
            yi=self.y_note(self.cursor.staff, self.cursor.note, octaves[self.cursor.staff]),
            h=int(self.h_note()),
            color=self.color_cursor,
        )
        # visual
        if self.visual.active:
            start, finish = self.get_visual_duration()
            staff_i = min(self.visual.staff, self.cursor.staff)
            staff_f = max(self.visual.staff, self.cursor.staff)
            batch.add_fill(
                xi=self.x_ticks(int(start)),
                xf=self.x_ticks(int(finish)),
                yi=self.y_note(staff_i, self.notes_per_staff()),
                yf=self.y_note(staff_f, -1),
                color=self.color_visual,
            )
        # text
        batch.draw(True)
        batch.add_text(
            self.text,
            x=self.margin,
            y=self.h_window - self.margin,
            anchor_y='bottom',
            h=self.text_size,
            color=self.color_text,
        )
        batch.add_text(
            f'{float(self.cursor.ticks / self.song.ticks_per_quarter):.2f}',
            x=self.w_window - self.margin,
            anchor_x = 'right',
            y=self.h_window - self.margin,
            anchor_y='bottom',
            h=self.text_size,
            color=self.color_text,
        )
        #
        batch.draw(False)
