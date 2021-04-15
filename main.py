import requests
import subprocess
import os

osu_directory = input('Osu directory location.\n-> ')
set_id = input('ID of map to download.\n-> ')

print('Downloading beatmap set.')
response = requests.get(f'https://api.chimu.moe/v1/download/{set_id}?n=0', allow_redirects=True)
print(response.url)
print('Beatmap set downloaded.')

os.makedirs('download')

print('Writing beatmap set to disc.')
download_out = open(f"download/{set_id}.osz", "wb")
download_out.write(response.content)
download_out.close()
print('Beatmap set written to disc.')

print('Extracting beatmap set.')
subprocess.run(["python3", "osz_converter.py", "download", f"{osu_directory}/Songs"])

print('Disposing of garbage.')
os.rmdir('download')
print('Garbage disposed.')
