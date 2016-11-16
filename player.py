#! /opt/anaconda3/bin/python3

import requests
import subprocess
import config
import sys
import os
from utils import timeoutgetch
import threading
import time

def wrapper(func, res):
	del res[:]
	res.append(func())

def get_tracks():
	if not config.owner_id:
		print('Add ID of user with awesome playlist in the config file')
	query = 'https://api.vk.com/method/audio.get?owner_id={}&access_token={}'.format(config.owner_id, config.token)
	r = requests.post(query)
	try:
		return [[x['artist'], x['title'], divmod(x['duration'], 60), x['url'].split('?')[0]] for x in r.json()['response'][1:] if 'url' in x]
	except:
		return []

res = []
thread = threading.Thread(target=wrapper, args=(get_tracks, res))
thread.start()

while thread.isAlive():
	for x in '-\|/':  
		b = 'Loading ' + x
		print (b, end='\r')
		time.sleep(0.1)

all_tracks = res[0]

if not all_tracks:
	print('Error: cannot get playlist of user {}'.format(config.owner_id))
	sys.exit(-1)

pointer = 0
while True:
	track = all_tracks[pointer]
	tmp = subprocess.Popen(['{}ffplay'.format(config.ffmpeg_path), '-nodisp', '-autoexit', track[3]], stderr=open(os.devnull, 'wb'))
	print('{}\n{} - {} [{}:{}]'.format('~'*50, track[0], track[1], track[2][0], track[2][1]))
	print('next [q] \tprev [w] \texit [x]')
	while tmp.poll() is None:
		x = timeoutgetch()
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
		if x == 0: break

	pointer += 1
