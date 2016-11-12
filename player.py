#! /opt/anaconda3/bin/python3

import requests
import subprocess
import config
import sys
import os
from utils import timeoutgetch
import threading
import time
import psutil

def wrapper(func, res):
	del res[:]
	res.append(func())

def get_tracks():
	query = 'https://api.vk.com/method/audio.get?owner_id={}&access_token=41398e48456b22943fe354e99c221f8b0a3f9b63cf944ba72c9a9dbc997549816c520dc2bb54ac090d9ae'.format(config.owner_id)
	r = requests.post(query)
	return  [[x['artist'], x['title'], divmod(x['duration'], 60), x['url'].split('?')[0]] for x in r.json()['response'][1:]]

res = []
thread = threading.Thread(target=wrapper, args=(get_tracks, res))
thread.start()

while thread.isAlive():
	for x in '-\|/':  
		b = 'Loading ' + x
		print (b, end='\r')
		time.sleep(0.1)

all_tracks = res[0]

pointer = 0
while True:
	track = all_tracks[pointer]
	tmp = subprocess.Popen(['{}ffplay'.format(config.ffmpeg_path), '-nodisp', '-autoexit', track[3]], stderr=open(os.devnull, 'wb'))
	ps_process = psutil.Process(pid=tmp.pid)
	print('{}\n{} - {} [{}:{}]'.format('~'*20, track[0], track[1], track[2][0], track[2][1]))
	print('prev(q)/next(w)/exit(x)')
	while not tmp.poll():
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
