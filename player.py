#! /opt/anaconda3/bin/python3

import requests
import subprocess
import config
import sys
import os
from utils import timeoutgetch, getch
import threading
import time
import psutil


def wrapper(func, res):
	del res[:]
	res.append(func())


def get_tracks():
	if not config.owner_id:
		print('Add ID of user with awesome playlist to the config file')

	if not config.owner_id.isdigit ():
		query = 'https://api.vk.com/method/users.get?user_ids={}'.format(config.owner_id)
		r = requests.post(query)
		config.owner_id = r.json()['response'][0]['uid']

	query = 'https://api.vk.com/method/audio.get?owner_id={}&access_token={}'.format(config.owner_id, config.token)
	r = requests.post(query)
	try:
		return [[x['artist'], x['title'], divmod(x['duration'], 60), x['url'].split('?')[0], x ['aid']] for x in r.json()['response'][1:] if 'url' in x]
	except:
		return []


def add_track(audio_id):
	query_add = 'https://api.vk.com/method/audio.add?audio_id={}&owner_id={}&access_token={}'.format(audio_id, config.owner_id, config.token)
	r = requests.post(query_add)
	return r.json()['response']

print('Choose wisely:')
[print('{}. {}'.format(num + 1, x)) for num, x in enumerate(config.owner_id)]

try:
	playlist_num = int(getch()) - 1
	config.owner_id = config.owner_id[playlist_num]
except:
	print('Error: bad input')
	sys.exit(1)

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
	print('Error: cannot get playlist of the user {}'.format(config.owner_id))
	sys.exit(-1)

AUTHOR = 0
SONG_NAME = 1
TIME = 2
URL_POSITION = 3

isPaused = False
isRepeat = False
pointer = 0

while True:
	track = all_tracks[pointer]
	tmp = subprocess.Popen(['{}ffplay'.format(config.ffmpeg_path), '-nodisp', '-autoexit', track[URL_POSITION]], stderr=open(os.devnull, 'wb'))
	psProcess = psutil.Process(pid=tmp.pid)

	print("{}\n{} - {} [{}:{}]".format('~'*40, track[AUTHOR], track[SONG_NAME], track[TIME][0], track[TIME][1]))
	print('prev[q]   next[w]   exit[x]   pause[p]   repeat[r]   add track[a]')
	if (isRepeat):
		print ("Repeat ON")
	
	while tmp.poll() is None:
		x = timeoutgetch()
		if x is None:
			continue

		if x == 'q':
			tmp.kill()
			if pointer < 1: pointer = 1
			pointer -= 2
			isPaused = False
			break
		elif x == 'w':
			tmp.kill()
			if pointer > len(all_tracks) - 1: pointer = len(all_tracks) - 1
			isPaused = False
			break
		elif x == 'x':
			tmp.kill()
			sys.exit()
			break
		elif x == 'p':
			isPaused = not isPaused
			if (isPaused):
				print ("Paused")
				psProcess.suspend()
			else:
				print ("Resumed")
				psProcess.resume()
		elif x == 'r':
			isRepeat = not isRepeat
			if (isRepeat):
				print ("Repeat ON")
			else:
				print ("Repeat OFF")
		elif x == 'a':
			ret = add_track (track [4])
			print ("Track added. The id is: {}".format (ret))

	if (tmp.poll () is not None and isRepeat):
		pass
	else:
		pointer += 1
