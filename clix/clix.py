import json
import xerox
from pyxhook import HookManager
from gui import clipboard
from multiprocessing import Process

# clipboard
clips = []
# number of active clix GUIs 
active = 0
# previously logged key
prev_Key = None
running = None

def OnKeyPress(event):
	global prev_Key, active, running
	if event.Key == 'space' and prev_Key == 'Control_L':
		if running == None or running.is_alive() == False:
			active = 1
			running = Process(target=clipboard,args=(clips,))
			running.start()
			prev_Key = None

	elif event.Key == 'c' and prev_Key == 'Control_L':
		text = xerox.paste(xsel = True)
		clips.append(text)
		try:
			if running is not None and running.is_alive() == True:
				running.terminate()
				running = Process(target=clipboard,args=(clips,))
				running.start()
		except Exception:
			pass
		print("You just copied: {}".format(text))
	elif event.Key == 'p':
		print(running.is_alive())
	else:
		prev_Key = event.Key

def main():
	new_hook = HookManager()
	new_hook.KeyDown = OnKeyPress
	new_hook.HookKeyboard()
	new_hook.start()


if __name__ == "__main__":
	main()
	

