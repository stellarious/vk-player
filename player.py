#! /opt/anaconda3/bin/python3

import requests
import subprocess
import config
import sys
import os
from utils import getch

query = 'https://api.vk.com/method/audio.get?owner_id={}&access_token={}'.format(config.owner_id, config.token)

r = requests.post(query)

all_tracks = [[x['artist'], x['title'], divmod(x['duration'], 60), x['url'].split('?')[0]] for x in r.json()['response'][1:]]

pointer = 0
while True:
	track = all_tracks[pointer]
	tmp = subprocess.Popen(['ffplay', '-nodisp', '-autoexit', track[3]], stderr=open(os.devnull, 'wb'))
	print('{}\n{} - {} [{}:{}]'.format('~'*20, track[0], track[1], track[2][0], track[2][1]))
	print('prev(q)/next(w)/exit(x)')
	while not tmp.poll():
		x = getch() #blocking input
		if x == 'q':
			tmp.kill()
			if pointer < 1: pointer = 1
			pointer -= 2
			break
		elif x == 'w':
			tmp.kill()
			if pointer > len(all_tracks) - 1: pointer = len(all_tracks) - 1
			break
		elif x == 'x':
			tmp.kill()
			sys.exit()
			break

	pointer += 1
