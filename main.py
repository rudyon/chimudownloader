import requests
import subprocess
import os
import json

osu_directory = input('Where are your osu! files?\n-> ')
search = input('Map(s) to install?\n-> ')

if ',' in search:
	print('Detected bulk download.')

	s = search.split(',')

	for i in s:
		search = i

		# Searches for beatmaps on the chimu.moe database.
		response = requests.get(f'https://api.chimu.moe/v1/search?query={search}&amount=1')
		response_parsed = json.loads(response.content)

		if response_parsed['code'] == 106:
			print('Beatmap not found.')
		else:
			response_parsed = response_parsed.get('data')[0]
			print(f"Found {response_parsed['Title']} - {response_parsed['Artist']} - {response_parsed['Creator']}.")
			response = requests.get(f"https://api.chimu.moe/v1/download/{response_parsed['SetId']}?n=0", allow_redirects=True)

			print('Attempting to create download directory.')
			try:
				os.makedirs('download')
				print('Created download directory.')
			except FileExistsError:
				print('Directory already exists.')

			print('Downloading beatmap set.')
			download_out = open(f"download/{response_parsed['SetId']}.osz", "wb")
			download_out.write(response.content)
			download_out.close()
			print('Beatmap set downloaded.')

			print('Extracting beatmap set.')
			# Calls to osz_converter.py and asks it to extract the beatmap file into the osu directory.
			subprocess.run(["python3", "osz_converter.py", "download", f"{osu_directory}/Songs"])

	print('Done.')

else:
	# Searches for beatmaps on the chimu.moe database.
	response = requests.get(f'https://api.chimu.moe/v1/search?query={search}&amount=1')
	response_parsed = json.loads(response.content)

	if response_parsed['code'] == 106:
		print('Beatmap not found.')
	else:
		response_parsed = response_parsed.get('data')[0]
		print(f"Found {response_parsed['Title']} - {response_parsed['Artist']} - {response_parsed['Creator']}.")
		response = requests.get(f"https://api.chimu.moe/v1/download/{response_parsed['SetId']}?n=0", allow_redirects=True)

		print('Attempting to create download directory.')
		try:
			os.makedirs('download')
			print('Created download directory.')
		except FileExistsError:
			print('Directory already exists.')

		print('Downloading beatmap set.')
		download_out = open(f"download/{response_parsed['SetId']}.osz", "wb")
		download_out.write(response.content)
		download_out.close()
		print('Beatmap set downloaded.')

		# Calls to osz_converter.py and asks it to extract the beatmap file into the osu directory.
		print('Extracting beatmap set.')
		subprocess.run(["python3", "osz_converter.py", "download", f"{osu_directory}/Songs"])

		print('Done.')
