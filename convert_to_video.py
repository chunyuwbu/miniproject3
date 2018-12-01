import os

def create(screen_name):
	try:
		command="ffmpeg -framerate 1  -i "+screen_name+"/%05d.jpg -vcodec mpeg4 -y "+screen_name+".mp4"
		os.system(command)
	except Exception as e:
		print(e)
		exit()