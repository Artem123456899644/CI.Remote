from wakeonlan import send_magic_packet
import sys
import FDP
version = 0.1
commandList = [{'name': "wol Pc",         'send': "WOL_pc1"},
			   {'name': "wol Server-1",   'send': "WOL_pc2"}
				]
class Programm:
	def __init__(self, req):
		if req is "WOL_pc1" or req is "/WOL_pc1":	send_magic_packet('00:E0:20:0E:A2:F4')
		elif req is "WOL_pc2" or req is "/WOL_pc2":	send_magic_packet('46:3E:38:26:21:13')
if __name__ == '__main__': Programm(req=FDP.Process.listenProcess)
	
else: Programm(req=sys.stdin())