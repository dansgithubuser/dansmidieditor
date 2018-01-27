#!/usr/bin/env python

import argparse
import os
import sys
import time

HOME=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HOME, '..', 'deps', 'danssfml', 'wrapper'))

from config import controls
import media

media.init(title="Dan's MIDI Editor")

def main():
	while not controls.done:
		while True:
			event=media.poll_event()
			if not event: break
			controls.input(event)
		controls.view.draw(media)
		time.sleep(0.01)

if __name__=='__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('--command', '-c', action='append', default=[])
	args=parser.parse_args()

	for i in args.command: controls.command(i)

	main()
