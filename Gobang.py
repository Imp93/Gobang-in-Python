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


#
#TODO: Problematik spielfeld um 30 px verkleinern
#mausposition wird bei klick erkannt, auf der linken seite 
#
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

def check_rules():
	
	return






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
