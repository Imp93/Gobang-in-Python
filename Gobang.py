#!/usr/bin/python

from tkinter import *
import math
import tkinter.messagebox

#globals
field = []
window = tkinter.Tk()
window.title("Gobang - now 22% more fun!")

#spielfeld linke seite
board_width = 570
board_height = 570
distance = 30

board = Canvas(window,width=board_width+distance, height=board_height+distance)
board.config(background="#FFFFFF")
board.pack(side=LEFT)


#spielerfarben w und b
current_player = "w"

#Funktionen


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
	print ("clicked at", pos_x, pos_y, "status is",field[pos_x][pos_y])
	if field[pos_x][pos_y] == "free":
		if current_player == "w":
			field[pos_x][pos_y] = "w"
			switch_player()
		else:
			field[pos_x][pos_y] = "b"
			switch_player()
	check_rules(pos_x,pos_y)
	board.delete("all")
	draw_board()
	return

def switch_player():
	global current_player
	if current_player=="w":
		current_player = "b"
	else:
		current_player = "w"
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
	
	for ck_field in surr:
		print(ck_field[0],ck_field[1])
	return

#check surroundings
def check_surrounding(pos_x,pos_y):
	#fields:
	#x-1/y-1	x/y-1	x+1/y-1
	#x-1/y		x/y		x+1/y
	#x-1/y+1	x/y+1	x+1/y+1
	print(pos_x-1," ",pos_x," ",pos_x+1)
	print(pos_y-1," ",pos_y," ",pos_y+1)
	surr_fields = []
	#fields above
	if (pos_y-1) > -1:
		if (pos_x-1) > -1: 
			surr_fields.append([[pos_x-1],[pos_y-1]])
		surr_fields.append([[pos_x],[pos_y-1]])
		if (pos_x+1) < 20:
			surr_fields.append([[pos_x+1],[pos_y-1]])
	#fields level
	if (pos_x-1) > -1:
		surr_fields.append([[pos_x-1],[pos_y]])
	if (pos_x+1) < 20:
		surr_fields.append([[pos_x+1],[pos_y]])
	#fields below
	if (pos_y+1) < 20:
		if (pos_x-1) > -1: 
			surr_fields.append([[pos_x-1],[pos_y+1]])
		surr_fields.append([[pos_x],[pos_y+1]])
		if (pos_x+1) < 20:
			surr_fields.append([[pos_x+1],[pos_y+1]])
	return surr_fields


#check field (x, y)
def check_field(pos_x, pos_y): return field[pos_x][pos_y]


def create_new_game():
	print("Neues Spiel")
	for row in range(0,19):
		collist = []
		for col in range(0,19):
			collist.append("free")
		
		field.append(collist)
	draw_board()
	
	return

	
#spiel-array, auf dem alle informationen gespeichert werden
#1.ebene x-koordinate
#2.ebene y-koordinate
#3.ebene zustand (white, black, free)


#mainframe = Frame(window, width=10, height=0) 
#mainframe.pack(side=TOP)

#erstellen des spielfelds
create_new_game()

#menü rechte seite
#menu = Canvas(window,width=300, height=spielfeld_height+abstand)
#menu.pack(side=RIGHT)
#btn1 = Button(menu,text="Neues Spiel",command = create_new_game)
#btn1.pack(side=TOP)

window.mainloop()
