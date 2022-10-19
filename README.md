# Dan's MIDI Editor

Dan's MIDI Editor has a few goals:
- an experiment in vim-like MIDI editing
- an alternative to MuseScore
- no silent mutations when you open a MIDI file
- open source & cross-platform

## todo
- recover previous features
    - need something like config, but don't use a made-up language
        - control module & pyglet input translation layer
    - View -> Editor
        - Editor is controlled by configured controls
        - Editor draws with pyglet
    - main should instantiate pyglet, controls, and Editor

- quantization
- niceties
    - indicator that more notes are off-screen
    - track 0 events
    - other events
    - horizontal scale shouldn't change when ticks per quarter does
