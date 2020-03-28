# Advanced Terminal Windowing Client
# An object oriented Wrapper for the tui library
from tui import *

MODE_OIL = 1
MODE_WATER = 0

class Window:


	def __init__(self,tag,height,width,y,x):
		self.tag = tag
		self.height = height
		self.width = width
		self.content = []
		self.pos_content = 0
		self.y = y # Relative to main window stdscr
		self.x = x # Relative to main window stdscr
		self.instance = window(self.height,self.width,self.y,self.x)
		boxify(self.instance,'*','*')
		# (0,0) is taken up by the border
		self.curs_pos = (1,1) # Track the current position of cursor in window
	
	# Write text to the given window
	# Pass in colors and attr as constants
	# from the tAPP class
	# Set cursor pos outside of paint after every call to paint()
	def paint(self,text,color,attr,mode=MODE_WATER):
		if mode == MODE_OIL:
			self.content.append((text,color,attr)) # Save the content of the window
		mvrender(self.curs_pos[0],self.curs_pos[1],text,self.instance,color,attr)
		#self.curs_pos = cursor_pos(self.instance)


	# Set the current cursor position of a window
	# to the next line of a window
	def newline(self):
		ln = self.curs_pos[0] + 1
		self.curs_pos = (ln,1)


	# Read input from the user, a limit is the edge of the window
	# Given by the window width	
	def read(self):
		edge = self.width
		usr_input = read(self.instance,self.curs_pos[0],self.curs_pos[1],edge)
		self.newline()	

		return user_input
		# self.paint(usr_input,set_color(1,YLW),BOLD)

	# TODO add left and right listeners
	# TODO Use the right and left listeners to switch context
	# Between windows, Global listener in the tApp class ?
	def listen(self):
		cloak()
		accept_keys(self.instance)
		c = byte(self.instance)

		if c == UP:
			if self.pos_content == 0:
				reject_keys(self.instance)
				uncloak()
				return c
			else:
				# Return previous entry to previous state
				# Unhighlited
				prev_text = self.content[self.pos_content][0]
				prev_cid = self.content[self.pos_content][1]
				self.paint(prev_text,prev_cid,BOLD,MODE_WATER)

				self.pos_content -= 1
				self.set_curs(self.curs_pos[0]-1,1)

				# Update new entry
				curr_text = self.content[self.pos_content][0]
				curr_cid = self.content[self.pos_content][1]
				curr_attr = self.content[self.pos_content][2]
				self.paint(curr_text,curr_cid,curr_attr|HILITE,MODE_WATER)
		elif c == DOWN:
			if self.pos_content == (len(self.content) - 1):
				reject_keys(self.instance)
				uncloak()
				return c
			else:
				prev_text = self.content[self.pos_content][0]
				prev_cid = self.content[self.pos_content][1]
				prev_attr = self.content[self.pos_content][2]
				self.paint(prev_text,prev_cid,BOLD,MODE_WATER)

				self.pos_content += 1
				self.set_curs(self.curs_pos[0]+1,1)

				curr_text = self.content[self.pos_content][0]
				curr_cid = self.content[self.pos_content][1]
				curr_attr = self.content[self.pos_content][2]
				self.paint(curr_text,curr_cid,curr_attr|HILITE,MODE_WATER)
		return c

	# Set position of the cursor to the top of the window		
	def reset_pos(self):
		self.curs_pos = (1,1)	

	
	def set_curs(self,y,x):
		self.curs_pos = (y,x)


	def clear(self):
		clear(self.instance)


	# Blocks application by calling unicurses.getch()
	# Waits for a a key to be pressed
	def wait(self):
		return byte(self.instance)
	

	# Row/Height x Col/Width
	def get_dimensions(self):
		return (self.height,self.width)


	# Relative positioning in main window stdscr
	def get_relative_pos(self):
		return (self.y,self.x)
	
	# Return the window instance of the Window
	def get_instance(self):
		return self.instance


	def get_curs_pos(self):
		return self.curse_pos # Line, Column

	def get_tag(self):
		return self.tag

	def get_content_pos(self):
		return self.pos_content


class Panel:
	
	# A panel is a container for a window
	# Windows must be directlry edited
	def __init__(self,window):
		self.instance = panel(window.instance)
		self.content = window
		self.tag = window.get_tag()

	def move_to(self,y,x):
		mvpanel(self.instance,y,x)



class tApp:

	# App will keep track of all panels
	def __init__(self):
		self.instance = setup() # tui stdscr
		self.content = [] # Panel Collection
		self.height,self.width = get_window_size(self.instance)

	# Pipe the creation of a window to a panel
	# in the app
	def pipe(self,window):
		self.content.append(Panel(window))
	
	def listen(self):
		unblock(self.instance)
		if byte(self.instance) == RESIZE:
			block(self.instance)
			return 'Window Resized'
		else:
			return 'Same'


	def wait(self):
		cloak()
		return byte()

	def close(self):
		terminate()

	def update(self):
		update()

'''
# Will be init in tApp class
stdscr = setup()
# Color pair ID must be handled by tApp class
cid = 1
win = Window('main',30,35,5,5)
win.paint('Hello, World',set_color(cid,RED),BOLD)
cid += 1
win.newline()
win.paint('On the next line',set_color(cid,GRN),UNDERLN|BOLD)
cid += 1
win.newline()
win.paint('>> ',set_color(cid,RED),NORMAL)
cid += 1
win.read()
win.wait()
terminate()
'''
# TODO check the legths of stdscr widht and height
# start the app
app = tApp()

# Create Windows and connect them to panels
main = Window('main',app.height,int(app.width*0.5),0,0)
right_pane = Window('pane',app.height - 20,int(app.width*0.3),0,main.width + 5)
app.pipe(main)
app.pipe(right_pane)

# Populate right pane with menu options
right_pane.paint('EXIT',set_color(1,WHT),BOLD|HILITE,MODE_OIL)
right_pane.newline()
right_pane.paint('TEST',set_color(2,RED),BOLD,MODE_OIL)
right_pane.newline()
right_pane.paint('TEST_2',set_color(3,GRN),BOLD,MODE_OIL)
right_pane.reset_pos()

while True:
	app.update()
	noblink()
	main.paint(app.listen(),set_color(4,YLW),BOLD|UNDERLN)
	c = right_pane.listen()
	if c == ENTER and right_pane.get_content_pos() == 0: 
		break
# end the app
app.close()
