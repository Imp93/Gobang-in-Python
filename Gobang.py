#!/usr/bin/python
from tkinter import *
import math
import tkinter.messagebox
from random import randint

game_window = tkinter.Tk()
game_window.title("Gobang")
menu = Menu(game_window)
game_window.config(menu=menu)
gamemenu = Menu(menu)
menu.add_cascade(label="Game", menu=gamemenu)
turninfo = Menu(menu)
menu.add_cascade(label="Gobang - Turn 1 - Player vs Player - Black's turn") #preselected

board_width = 570
board_height = 570
distance = 30
board = Canvas(game_window,width=board_width+distance, height=board_height+distance)
board.config(background="#FFFFFF")
board.pack(expand=NO, fill=Y)

def get_pos_x(event):
	x_pos = (event.x/30)
	x_rest = (x_pos-int(x_pos))*10
	if x_rest < 5:x_pos = x_pos-1
	if x_pos >= 19:x_pos = 18
	return int(x_pos)

def get_pos_y(event):
	y_pos = (event.y/30)
	y_rest = (y_pos-int(y_pos))*10
	if y_rest < 5:y_pos = y_pos-1
	if y_pos >= 19:y_pos = 18
	return int(y_pos)
	
def destroy_o_screen():
	global o_screen
	try: o_screen
	except NameError: o_screen = None
	if o_screen is not None:o_screen.destroy()

def destroy_w_screen():
	global w_screen
	try: w_screen
	except NameError: w_screen = None
	if w_screen is not None:w_screen.destroy()

def set_stone(event):
	pos_x = get_pos_x(event)
	pos_y = get_pos_y(event)
	if field[pos_x][pos_y] == "free":
		field[pos_x][pos_y] = current_player
		draw_board()
		if check_rules(pos_x,pos_y) == 1:winscreen()
		if ai_level == 1: random_ai_turn()
		if ai_level == 2: ai_turn()
		switch_player()

def switch_player():
	destroy_o_screen()
	set_player("b") if current_player == "w" else set_player("w")
	refresh_turninfo()

def draw_board():
	board.delete("all")
	for row in range(0,20):board.create_line(row*distance, distance, row*distance, board_height, fill="#000000")
	for col in range(0,20):board.create_line(distance, col*distance, board_width, col*distance, fill="#000000")
	for row in range(0,19):
		for col in range(0,19):
			if field[row][col] == "w":board.create_oval((row+1)*distance-(distance/2), (col+1)*distance-(distance/2), (row+1)*distance+(distance/2), (col+1)*distance+(distance/2),fill="#fff")
			if field[row][col] == "b":board.create_oval((row+1)*distance-(distance/2), (col+1)*distance-(distance/2), (row+1)*distance+(distance/2), (col+1)*distance+(distance/2),fill="#000")
	if game_end == 0:board.bind("<1>",set_stone)

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
						if dir_field[2][0] == current_player:dir_win_count = dir_win_count+1
						else: break
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
	#look for win  win1 = -  win2 = I  win3 = \  win4 = /
	win1 = win2 = win3 = win4 = 0
	for win_dir in win_count:
		if win_dir[1] == 0:win1 = win1+win_dir[2]
		if win_dir[0] == 0:win2 = win2+win_dir[2]
		if win_dir[0] == -1 and win_dir[1] == -1:win3 = win3+win_dir[2]
		if win_dir[0] == 1 and win_dir[1] == 1:win3 = win3+win_dir[2]
		if win_dir[0] == 1 and win_dir[1] == -1:win4 = win4+win_dir[2]
		if win_dir[0] == -1 and win_dir[1] == 1:win4 = win4+win_dir[2]
	if win1 > 3 or win2 > 3 or win3 > 3 or win4 > 3: 
		win = 1
		return win

def check_surrounding(pos_x,pos_y):
	#fields:
	#x-1/y-1	x/y-1	x+1/y-1
	#x-1/y		x/y		x+1/y
	#x-1/y+1	x/y+1	x+1/y+1
	surr_fields = []
	if (pos_y-1) > -1:
		if (pos_x-1) > -1: surr_fields.append([[pos_x-1],[pos_y-1]])
		surr_fields.append([[pos_x],[pos_y-1]])
		if (pos_x+1) < 19:surr_fields.append([[pos_x+1],[pos_y-1]])
	if (pos_x-1) > -1:surr_fields.append([[pos_x-1],[pos_y]])
	if (pos_x+1) < 19:surr_fields.append([[pos_x+1],[pos_y]])
	if (pos_y+1) < 19:
		if (pos_x-1) > -1: surr_fields.append([[pos_x-1],[pos_y+1]])
		surr_fields.append([[pos_x],[pos_y+1]])
		if (pos_x+1) < 19:surr_fields.append([[pos_x+1],[pos_y+1]])
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
	return "oob" #out of bound

def check_field(pos_x, pos_y): return field[pos_x][pos_y]

def check_field_value(pos_x, pos_y):
	value = 0
	surrounding = check_surrounding(pos_x,pos_y)
	for ck_field in surrounding:
		field_owner = check_field(ck_field[0][0],ck_field[1][0])
		#position for direction
		dir_x = ck_field[0][0]-pos_x
		dir_y = ck_field[1][0]-pos_y
		#direction own stone
		if field_owner != "free":
			if field_owner == current_player:
				value=value+10 #own stone
				fields_dir = check_direction(pos_x,dir_x,pos_y,dir_y)
				anti_fields_dir = check_direction(pos_x,dir_x*-1,pos_y,dir_y*-1)
				dir_count = 1
				if fields_dir != "oob":
					for field_dir in fields_dir:
						if field_dir[2][0] == current_player:
							value = value+10 #adjacent own stone after
							if dir_count == 3:
								value = value+30 #bonus 4th stone
								if anti_fields_dir[0][2][0] == current_player:value = value+100 #bonus for win with 5th stone
							if dir_count == 4:value = value+100 #bonus for win with 5th stone
						else: break
						dir_count = dir_count+1 #stone number after first
						if field_dir[2][0] == "free":break
			#direction enemy stone
			if field_owner != current_player:
				value=value+10 #enemy stone
				fields_dir = check_direction(pos_x,dir_x,pos_y,dir_y)
				anti_fields_dir = check_direction(pos_x,dir_x*-1,pos_y,dir_y*-1)
				dir_count = 1
				if fields_dir != "oob":
					for field_dir in fields_dir:
						if field_dir[2][0] != current_player:
							if dir_count == 3:
								value = value+30 #3 enemy stones in a row
								if anti_fields_dir[0][2][0] != current_player:value = value+100 #interrupt enemys winning
							if dir_count == 4:value = value+90 #4 enemy stones in a row, enemy is winning!
							if dir_count == 2:
								if anti_fields_dir[0][2][0] != current_player and anti_fields_dir[0][2][0] != "free":
									value= value+20 #enemy tries something
									if len(anti_fields_dir) > 1:
										if anti_fields_dir[1][2][0] != current_player and anti_fields_dir[1][2][0] != "free":
											value = value+60 #interrupt enemys winning
						if field_dir[2][0] == current_player:
							if dir_count == 3:value = value+30 #can remove enemy stones or cancle enemy winning
							break #no danger after that
						dir_count = dir_count+1
						if field_dir[2][0] == "free":break
	return value

def refresh_turninfo():
	global current_player
	global ai_level
	global turn_count
	global game_end
	
	turn_count = turn_count+1
	game_mode = "Player vs Player"
	cur_player = "Black" if current_player == "b" else "White"
	if ai_level == 0: game_mode = "Player vs Player"
	if ai_level == 1: game_mode = "Player vs Random"
	if ai_level == 2: game_mode = "Player vs Normal AI"
	menu.entryconfig(2,label="Turn "+str(turn_count)+" - "+game_mode+" - "+cur_player+"'s turn")

def set_ai(level):
	global ai_level
	destroy_o_screen()
	ai_level = level
	if ai_level == 0: game_mode = "Player vs Player"
	if ai_level == 1: game_mode = "Player vs Random"
	if ai_level == 2: game_mode = "Player vs Normal AI"
	menu.entryconfig(2,label="Turn 1 - "+game_mode+" - Black's turn")

def random_ai_turn():
	rand_x = randint(0,18)
	rand_y = randint(0,18)
	if check_field(rand_x,rand_y) == "free":
		switch_player()
		field[rand_x][rand_y] = current_player
		draw_board()
		if check_rules(rand_x,rand_y) == 1:winscreen()
	else: random_ai_turn()

def ai_turn():
	switch_player()
	possible_plays = []
	best_plays = []
	for ai_pos_x in range(0,18):
		for ai_pos_y in range(0,18):
			if check_field(ai_pos_x,ai_pos_y) == "free":
				field_value = check_field_value(ai_pos_x,ai_pos_y)
				if field_value > 0: possible_plays.append([ai_pos_x,ai_pos_y,field_value])
	max_value = max(value for [x,y,value] in possible_plays)
	for play in possible_plays:
		if play[2] == max_value:
			best_plays.append(play)
	play_nr = randint(0,len(best_plays))
	field[best_plays[play_nr-1][0]][best_plays[play_nr-1][1]] = current_player
	draw_board()
	if check_rules(best_plays[play_nr-1][0],best_plays[play_nr-1][1]) == 1:winscreen()

def set_player(player):
	global current_player
	current_player = player

def winscreen():
	global game_end
	global w_screen
	board.unbind("<1>")
	player="Black" if current_player == "b" else "White"
	game_window.title("Gobang - "+player+" has won") #does not work
	w_screen = Toplevel(game_window)
	w_screen.title("Player "+player+" has won!")
	label = Label(w_screen, text="Player "+player+" has won!\nNew Game?\n", width=35)
	label.pack(side=TOP)
	button = Button(w_screen, text="New Game", command=create_new_game)
	button.pack(side=BOTTOM)
	game_end = 1
	w_screen.geometry('%dx%d+%d+%d' % (175,75,250,250))

def create_new_game():
	global field
	global current_player
	global game_end
	global turn_count
	global o_screen
	destroy_w_screen()
	current_player = "b" #playercolours b and w
	set_ai(0)
	turn_count = 1
	game_end = 0
	field = []
	for row in range(0,19):
		collist = []
		for col in range(0,19):
			collist.append("free")
		field.append(collist)
	draw_board()
	game_window.title("Gobang")
	o_screen = Toplevel(game_window)
	o_screen.title("Options")
	o_screen.lift(aboveThis=game_window)
	o_label = Label(o_screen, text="Choose gamemode", width=25).pack(side=TOP)
	bt1 = Button(o_screen, text = "Player vs Player", command=lambda: set_ai(0), width=25).pack(side=TOP)
	bt2 = Button(o_screen, text = "Player vs Random", command=lambda: set_ai(1), width=25).pack(side=TOP)
	bt3 = Button(o_screen, text = "Player vs AI", command=lambda: set_ai(2), width=25).pack(side=TOP)
	o_screen.geometry('%dx%d+%d+%d' % (175,100,250,250))

gamemenu.add_command(label="New Game", command=create_new_game)
gamemenu.add_command(label="Exit", command=game_window.quit)

create_new_game()
game_window.mainloop()