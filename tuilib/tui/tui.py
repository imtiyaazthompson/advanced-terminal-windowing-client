import unicurses as uc
from time import sleep
from random import seed,randint

#TODO fix read function, get unicurses method to read

# Attributes
# Combine attributes with OR |
NORMAL 	= uc.A_NORMAL        # Normal display (no highlight)
HILITE 	= uc.A_STANDOUT      # Best highlighting mode of the terminal.
UNDERLN = uc.A_UNDERLINE     # Underlining
REV 	= uc.A_REVERSE       # Reverse video
BLINK 	= uc.A_BLINK         # Blinking
DIM 	= uc.A_DIM           # Half bright
BOLD 	= uc.A_BOLD          # Extra bright or bold
PROTC	= uc.A_PROTECT       # Protected mode
INV	= uc.A_INVIS         # Invisible or blank mode
ALT	= uc.A_ALTCHARSET    # Alternate character set
EXTCHR	= uc.A_CHARTEXT      # Bit-mask to extract a character

# Colors
BLK = uc.COLOR_BLACK
RED = uc.COLOR_RED
GRN = uc.COLOR_GREEN
YLW = uc.COLOR_YELLOW
BLU = uc.COLOR_BLUE
MAG = uc.COLOR_MAGENTA
CYA = uc.COLOR_CYAN
WHT = uc.COLOR_WHITE
DEFAULT_COLOR = 0

OFFSET = 1

# ASCII CODE - KEYS
ENTER = 10

# Common Keys
BKSPC = uc.KEY_BACKSPACE
DOWN = uc.KEY_DOWN
UP = uc.KEY_UP
LEFT = uc.KEY_LEFT
RIGHT = uc.KEY_RIGHT
RESIZE = uc.KEY_RESIZE

# Initialize curses
def init():
	return uc.initscr()


# Setup Curses by initializing it and starting any
# special curses functions
def setup():
	stdscr = init()
	uc.start_color()
	uc.init_pair(DEFAULT_COLOR,-1,-1)
	uc.use_default_colors()
	uc.keypad(stdscr, True)
	return stdscr

# Create a new window consisting of lines and columns
# That start on the main window stdscr at start_
def window(lines,columns,start_ln,start_col):
	return uc.newwin(lines,columns,start_ln,start_col)


# Create a box around any given window
def boxify(window,h_char='*',v_char='*'):
	uc.box(window,ord(h_char),ord(v_char))
	mvcursor(OFFSET,OFFSET,window)


# Panels are containers for windows
# Allows multiple windows to be displayed at
# once
# To update any changes to the panel after
# Changes to the respective windows have been made
# Call update
# Panels are useful for displaying multiple 
# windows at once, since we make changes to the 
# windows and the call update() to reflect those 
# changes to the corresponding panels
def panel(window):
	p = uc.new_panel(window)
	return p


# Render window updates to panels
# Usually called within main loop
def update():
	uc.update_panels()
	uc.doupdate()


# Waits for user input of one character
# Blocks any currently running loop
# Returns the ascii character value
# For the character consumed	
def byte(window=None,y=-1,x=-1):
	if window == None:
		return uc.getch()
	elif y == -1 and x == -1:
		return uc.wgetch(window)
	else:
		return uc.mvwgetch(window,y,x)

# Set getch() to not block
def unblock(window):
	uc.nodelay(window,True)

# Set getch() to block
def blokc(window):
	uc.nodelay(window,False)

# Return the ASCII character
# from the ascii code ord_char
def rvord(ord_char):
	return chr(ord_char)


# Move the cursor in the terminal window
# To the specified line and column of the
# terminal window
def mvcursor(line,column,window=None):
	if window == None:
		uc.move(line,column)
	else:
		uc.wmove(window,line,column)


# Get the current cursor position in
# the given window
def cursor_pos(window):
	return uc.getyx(window)


# Move a panel to a specific line
# and column
def mvpanel(panel,line,column):
	uc.move_panel(panel,line,column)


# Move the cursor to the specified 
# line and column then print out
# the output at that position
# Overwrites with no clear
# Daefualt None when outputting to main terminal window
def mvrender(line,column,output,window=None,color=DEFAULT_COLOR,attr=NORMAL):
	if window == None:
		uc.attron(uc.COLOR_PAIR(color))
		uc.attron(attr)
		uc.mvaddstr(line,column,output)
		uc.attroff(attr)
		uc.attroff(uc.COLOR_PAIR(color))
	else:
		uc.wattron(window,uc.COLOR_PAIR(color))
		uc.wattron(window,attr)
		uc.mvwaddstr(window,line,column,output)
		uc.wattroff(window,attr)
		uc.wattroff(window,uc.COLOR_PAIR(color))
		

# Write to the curses terminal window
# stdscr by defualt
# Overwrites previously rendered text
# and does not clear
# Default None when outputting to main terminal window
def render(output,window=None,color=DEFAULT_COLOR,attr=NORMAL):
	if window == None:
		uc.attron(uc.COLOR_PAIR(color))
		uc.attron(attr)
		uc.addstr(output)
		uc.attroff(attr)
		uc.attroff(uc.COLOR_PAIR(color))
	else:
		uc.wattron(window,uc.COLOR_PAIR(color))
		uc.wattron(window,attr)
		uc.waddstr(window,output)
		uc.wattroff(window,attr)
		uc.wattroff(window,uc.COLOR_PAIR(color))

# TODO handle backspace to delete last character
# TODO handle movement to traverse string to edit	
def read(window,ln,col,edge):
	st = uc.wgetstr(window)
	return st.decode('utf-8')
	

# Return a tuple with
# (lines,columns)
def get_window_size(stdscr):
	return uc.getmaxyx(stdscr)


# Create a color pair and return its
# With background defaulted to -1
# which is the terminals default BG
# Return the pair ID
# A color must be set before 
# calling a render function to
# render in that color
def set_color(pid,fg,bg=-1):
	uc.init_pair(pid,fg,bg)
	return pid


# Clear a given window
def clear(window):
	uc.wclear(window)


# Turns echoing off
# Will not be able to see what 
# is being types
def cloak():
	uc.noecho()

# Turn echoing on
def uncloak():
	uc.echo()


# Turn cursor blinking off
def noblink():
	uc.curs_set(False)


# Turn curson blinking on
def blink():
	uc.curs_set(True)


# Consume special keys such as arrow keys
def accept_keys(window):
	uc.keypad(window,True)


# Do not consume special keys
def reject_keys(window):
	uc.keypad(window,False)


# Create a delay of n seconds
def delay(n):
	sleep(n)


def save(window,fname):
	# TODO safety check on dir /windows/
	with open('windows/{}.win'.format()) as f:
		uc.putwin(f)

def load(fname):
	# TODO load a file
	pass


# Return a random number between
# s and e
def rand(s,e):
	#seed(1)
	return randint(s,e)


# Terminate curses terminal window
def terminate():
	uc.endwin()

def main():
	stdscr = setup()
	boxify(stdscr,'|','+')
	test_0 = window(20,20,5,5)
	boxify(test_0,'-','+')
	test_1 = window(20,20,5,35)
	boxify(test_1,'+','-')
	panels = [panel(stdscr),panel(test_0),panel(test_1)]
	#anchor = window(5,25,20,15)
	#boxify(anchor)

	#main_panel = panel(stdscr)

	#mvcursor(1,10)
	#render('Hello, World!')
	#mvrender(2,4,'Curses Yay!')
	#c = byte()
	#mvrender(3,3,'Escaped with {}'.format(str(c)))
	#i = 2
	#while True:
	#	c = byte()
	#	if c == 27:
	#		break
	#	else:
	#		mvrender(0,0,'Pressed {}'.format(rvord(c)))
	#	mvrender(i,0,'ASCII code: {}, ASCII char: {}\n'.format(str(c),rvord(c)))
	#	i += 1

	#ln,col = get_window_size(stdscr)
	#for i in range(ln):
	#	for j in range(col):
	#		mvrender(i,j,'x')
	i,j = (0,0)
	uncloak()
	strb = ''
	while True:
		mvrender(2,2,'>',test_1,set_color(1,RED),BOLD)
		strb += str(c)
		update()	

	byte()
	terminate()

if __name__ == '__main__':
	main()
