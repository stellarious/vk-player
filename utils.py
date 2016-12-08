import os, time

if os.name == 'nt':
	import msvcrt
else:
	import sys
	import termios
	import atexit
	from select import select


class KBHit:	
	def __init__(self):
	# Creates a KBHit object that you can call to do various keyboard things.
		if os.name == 'nt':
			pass
		
		else:
			# Save the terminal settings
			self.fd = sys.stdin.fileno()
			self.new_term = termios.tcgetattr(self.fd)
			self.old_term = termios.tcgetattr(self.fd)
		
			# New terminal setting unbuffered
			self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
		
			# Support normal-terminal reset at exit
			atexit.register(self.set_normal_term)

	def set_normal_term(self):
		if os.name == 'nt':
			pass
		else:
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


	def getch(self):
		''' Returns a keyboard character after kbhit() has been called.
			Should not be called in the same program as getarrow().
		'''

		s = ''

		if os.name == 'nt':
			return msvcrt.getch().decode('utf-8')
		
		else:
			return sys.stdin.read(1)
		

	def kbhit(self):
		if os.name == 'nt':
			return msvcrt.kbhit()
		else:
			dr,dw,de = select([sys.stdin], [], [], 0)
			return dr != []

def timeoutgetch (timeout = 0.01):
	kb = KBHit()
	char = None
	startTime = time.time()

	while time.time() - startTime < timeout:
		if kb.kbhit():
					char = kb.getch()

	kb.set_normal_term()
	return char

def getch():
	try:
		# for Windows-based systems
		import msvcrt # If successful, we are on Windows
		return msvcrt.getch()

	except ImportError:
		# for POSIX-based systems (with termios & tty support)
		import tty, sys, termios  # raises ImportError if unsupported

		fd = sys.stdin.fileno()
		oldSettings = termios.tcgetattr(fd)

		try:
			tty.setraw(fd)
			answer = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

		return answer 