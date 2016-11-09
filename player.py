import requests
from subprocess import call
import config

query = 'https://api.vk.com/method/audio.get?owner_id={}&access_token={}'.format(config.owner_id, config.token)

r = requests.post(query)

all_tracks = [[x['artist'], x['title'], x['url'].split('?')[0]] for x in r.json()['response'][1:]]

for track in all_tracks[:3]:
	with open('%s.mp3' % track[1], 'wb') as f:
		response = requests.get(track[2], stream=True)

		if not response.ok:
			print('ERROR')

		for block in response.iter_content(1024):
			f.write(block)
			print('.', end='')

		print('OK')

	#tmp = call(['ffplay', '-nodisp', '-autoexit', '%s.mp3' % track[1]])
	tmp = call(['mpg321', '-o', 'alsa', '%s.mp3' % track[1]])
