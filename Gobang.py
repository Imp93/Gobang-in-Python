#!/usr/bin/python

from tkinter import *
import math
import tkinter.messagebox

#globals
field = []
game_window = tkinter.Tk()
game_window.title("Gobang - hurry up and work already, please!")
menu = Menu(game_window)
game_window.config(menu=menu)
gamemenu = Menu(menu)
menu.add_cascade(label="Game", menu=gamemenu)

#field left side
board_width = 570
board_height = 570
distance = 30

board = Canvas(game_window,width=board_width+distance, height=board_height+distance)
board.config(background="#FFFFFF")
board.pack(side=LEFT)

#statistics and informations right side
stats_width = 230
stats_height = 570

stats_pane = Frame(game_window,width=stats_width, height=stats_height)
stats_pane.pack(side=LEFT)
stats_current_player = Label(stats_pane,text="Black", width=30).pack(side=TOP)

#playercolors w und b
current_player = "b"

#AI-difficulties
#0 = no AI (Player vs Player)
#1 = random AI (sets stones at random)
#2 = full AI (Player vs AI)
ai_level = 0

#functions

def get_pos_x(event):
	x_pos = (event.x/30)
	x_rest = (x_pos-int(x_pos))*10
	if x_rest < 5:
		x_pos = x_pos-1
	if x_pos >= 19:
		x_pos = 18
	return int(x_pos)

def get_pos_y(event):
	y_pos = (event.y/30)
	y_rest = (y_pos-int(y_pos))*10
	if y_rest < 5:
		y_pos = y_pos-1
	if y_pos >= 19:
		y_pos = 18
	return int(y_pos)
	
def set_stone(event):
	pos_x = get_pos_x(event)
	pos_y = get_pos_y(event)
#	print ("clicked at", pos_x, pos_y, "status is",field[pos_x][pos_y])
	if field[pos_x][pos_y] == "free":
		if current_player == "w":
			field[pos_x][pos_y] = "w"
		else:
			field[pos_x][pos_y] = "b"
		win = check_rules(pos_x,pos_y)
		board.delete("all")
		draw_board()
		if win == 1:
			if current_player == "b": player="Black"
			else: player="White"
			winscreen(player)
			board.unbind("<1>")
		if ai_level == 1: random_ai_turn()
		if ai_level == 2: ai_turn()
		switch_player()
	return

def switch_player():
	if current_player=="w":set_player("b")
	else:set_player("w")
	
	#TODO: stuff when player switches (information current player)
	return

def draw_board():
	board.delete("all")
	for row in range(0,20):
		board.create_line(row*distance, distance, row*distance, board_height, fill="#000000")

	for col in range(0,20):
		board.create_line(distance, col*distance, board_width, col*distance, fill="#000000")
	
	for row in range(0,19):
		for col in range(0,19):
			if field[row][col] == "w":
				board.create_oval((row+1)*distance-(distance/2), (col+1)*distance-(distance/2), (row+1)*distance+(distance/2), (col+1)*distance+(distance/2),fill="#fff")
			if field[row][col] == "b":
				board.create_oval((row+1)*distance-(distance/2), (col+1)*distance-(distance/2), (row+1)*distance+(distance/2), (col+1)*distance+(distance/2),fill="#000")
			
	board.bind("<1>",set_stone)
	return 

def check_rules(pos_x,pos_y):
	surr = check_surrounding(pos_x,pos_y)
	win_count = []
	for ck_field in surr:
		if check_field(ck_field[0][0],ck_field[1][0]) != "free":
			if check_field(ck_field[0][0],ck_field[1][0]) == current_player:
				direction_x = ck_field[0][0]-pos_x
				direction_y = ck_field[1][0]-pos_y
				dir_win_count = 0
				dir = check_direction(pos_x,direction_x,pos_y,direction_y)
				if dir != "oob":
					for dir_field in dir:
						if dir_field[2][0] == current_player:
							dir_win_count = dir_win_count+1
				
				win_count.append([direction_x,direction_y,dir_win_count])
			else:
				#remove enemy stones (2 in direction), if stone after that in that direction is my own
				direction_x = ck_field[0][0]-pos_x
				direction_y = ck_field[1][0]-pos_y
				dir = check_direction(pos_x,direction_x,pos_y,direction_y)
				if dir != "oob":
					if len(dir) > 2:
						if dir[0][2][0] != current_player and dir[1][2][0] != current_player and dir[2][2][0] == current_player:
							field[dir[0][0][0]][dir[0][1][0]] = "free"
							field[dir[1][0][0]][dir[1][1][0]] = "free"
	#look for win
	#win1 = -
	#win2 = I
	#win3 = \
	#win4 = /
	#win1 = win_count[-1][0]
	win1 = win2 = win3 = win4 = 0
	for win_dir in win_count:
		if win_dir[1] == 0:
			win1 = win1+win_dir[2]
		if win_dir[0] == 0:
			win2 = win2+win_dir[2]
		if win_dir[0] == -1 and win_dir[1] == -1:
			win3 = win3+win_dir[2]
		if win_dir[0] == 1 and win_dir[1] == 1:
			win3 = win3+win_dir[2]
		if win_dir[0] == 1 and win_dir[1] == -1:
			win4 = win4+win_dir[2]
		if win_dir[0] == -1 and win_dir[1] == 1:
			win4 = win4+win_dir[2]
	
	if win1 > 3 or win2 > 3 or win3 > 3 or win4 > 3: 
		win = 1
		return win
	return

#check surroundings
def check_surrounding(pos_x,pos_y):
	#fields:
	#x-1/y-1	x/y-1	x+1/y-1
	#x-1/y		x/y		x+1/y
	#x-1/y+1	x/y+1	x+1/y+1
	surr_fields = []
	#fields above
	if (pos_y-1) > -1:
		if (pos_x-1) > -1: 
			surr_fields.append([[pos_x-1],[pos_y-1]])
		surr_fields.append([[pos_x],[pos_y-1]])
		if (pos_x+1) < 19:
			surr_fields.append([[pos_x+1],[pos_y-1]])
	#fields level
	if (pos_x-1) > -1:
		surr_fields.append([[pos_x-1],[pos_y]])
	if (pos_x+1) < 19:
		surr_fields.append([[pos_x+1],[pos_y]])
	#fields below
	if (pos_y+1) < 19:
		if (pos_x-1) > -1: 
			surr_fields.append([[pos_x-1],[pos_y+1]])
		surr_fields.append([[pos_x],[pos_y+1]])
		if (pos_x+1) < 19:
			surr_fields.append([[pos_x+1],[pos_y+1]])
	return surr_fields

def check_direction(pos_x,dir_x,pos_y,dir_y):
	dir_field = []
	if(pos_y+dir_y) > -1 and (pos_y+dir_y) < 19:
		if(pos_x+dir_x) > -1 and (pos_x+dir_x) < 19:
			dir_field.append([[pos_x+dir_x],[pos_y+dir_y],[check_field(pos_x+dir_x,pos_y+dir_y)]])
			next_dir = check_direction(pos_x+dir_x,dir_x,pos_y+dir_y,dir_y)
			if next_dir != "oob":
				if next_dir[0][2][0] != "free":
					for current_dir in next_dir:
						dir_field.append(current_dir)
			return dir_field
	return "oob"

#check field (x, y)
def check_field(pos_x, pos_y): return field[pos_x][pos_y]

def set_ai(level,o_screen=""):
	global ai_level
	print("ai_level: ",level)
	if o_screen != "":o_screen.destroy()
	ai_level = level
	return

def random_ai_turn():
	
	return

def set_player(player):
	global current_player
	current_player = player
	return

def winscreen(player):
	winscreen = Toplevel(game_window)
	winscreen.title("Player "+player+" has won!")
	label = Label(winscreen, text="Player "+player+" has won!\nNew Game?\n", width=35)
	label.pack(side=TOP)
	button = Button(winscreen, text="New Game", command= lambda: create_new_game(winscreen))
	button.pack(side=BOTTOM)
	return

def create_new_game(winscreen = ""):
	global field
	global current_player
	if winscreen != "": winscreen.destroy()
	current_player = "b"
	set_ai(0)
	
	field = []
	for row in range(0,19):
		collist = []
		for col in range(0,19):
			collist.append("free")
		field.append(collist)
	draw_board()
	
	o_screen = Toplevel(game_window)
	o_screen.title("Optionen")
	o_screen.lift(aboveThis=game_window)
	o_label = Label(o_screen, text="Spielmodus wählen", width=25).pack(side=TOP)
	bt1 = Button(o_screen, text = "Spieler gegen Spieler", command=lambda: set_ai(0,o_screen), width=25).pack(side=TOP)
	bt2 = Button(o_screen, text = "Spieler gegen Zufalls-KI", command=lambda: set_ai(1,o_screen), width=25).pack(side=TOP)
	bt3 = Button(o_screen, text = "Spieler gegen KI", command=lambda: set_ai(2,o_screen), width=25).pack(side=TOP)
	
	return

gamemenu.add_command(label="New Game", command=create_new_game)
gamemenu.add_command(label="Exit", command=game_window.quit)

#start the game!
create_new_game()

game_window.mainloop()
