from pygame.mixer import find_channel

from config import *


def p2p_dist(A,B):
	return sqrt((B.x-A.x)**2 + (B.y-A.y)**2)

def safe_access(List, index):
	return List[min(index, len(List))-1]

def play_panned(sound, x):
	channel = find_channel()
	channel.set_volume(1 - (x+PLAY_AREA_SIZE/2) / (2*PLAY_AREA_SIZE), (x+PLAY_AREA_SIZE/2) / (2*PLAY_AREA_SIZE))
	channel.play(sound)
	
def time_to_string(t):
	ms = t%1000
	s = int(t/1000)%60
	m = int(t/60000)
	return str(m).zfill(2) + ":" + str(s).zfill(2) + ":" + str(ms).zfill(3)

