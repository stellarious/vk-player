#! /opt/anaconda3/bin/python3

import requests
import subprocess
import config
import sys
import os
from utils import getch

query = 'https://api.vk.com/method/audio.get?owner_id={}&access_token={}'.format(config.owner_id, config.token)

r = requests.post(query)

all_tracks = [[x['artist'], x['title'], x['url'].split('?')[0]] for x in r.json()['response'][1:]]

for track in all_tracks[:]:
	tmp = subprocess.Popen(['ffplay', '-nodisp', '-autoexit', track[2]], stderr=open(os.devnull, 'wb'))
	print('{}\n{} - {}'.format('~'*20, track[0], track[1]))
	print('next(q)/exit(x)')
	while tmp.poll() == None:
		x = getch()
		if x == 'q':
			tmp.kill()
			break
		elif x == 'x':
			tmp.kill()
			sys.exit()
			break
