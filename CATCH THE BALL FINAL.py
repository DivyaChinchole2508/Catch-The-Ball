# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 16:26:08 2020

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 15:35:48 2020

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 11:38:52 2020

@author: Admin
"""
#importing tkinter to create GUI for user to enter their name
import tkinter as tk
# importing pygame
import pygame
# importing random
import random
# importing matplotlib
import matplotlib.pyplot as plt
#initialising pygame library 
pygame.init()


# intialising a few colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
pink = (255,0,127)
blue = (0,0,255)
purple = (127,0,255)
yellow = (255,255,0)
# initialising clock to track time
clock = pygame.time.Clock()
# setting a variable score to keep track of score
global score 
score = 0
global intro
intro = True
# function to extract scores of previous attemps from file
def CheckData():
    # opening the file
    file = open("score.txt")
    #creating list to append names and scores
    lst = []
    # reading scores and names
    for line in file:
        wrds = line.split(sep=",")
        lst.append((wrds[0],int(wrds[1])))
        # sorting bt scores
    lst.sort(key = lambda x:x[1], reverse = True)
    # getting top five
    leaderboard = lst[:5]
    #print(leaderboard)
    return leaderboard,lst
# function to display graph
def displayGraph(Scr):
    dispOn = True # variable to keep track of how long the display is shown
    while dispOn:
        # getting events
        for event in pygame.event.get():
            # checking for exiting the screen
            if event.type == pygame.QUIT:
                dispOn = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # checking for backspace
                if event.key == pygame.K_BACKSPACE:
                    dispOn=False
                    # going to previous screen
                    EndScreen(Scr)
        # configuraing the window
        gameWin.fill(black)
        # loading the graph
        imageGraph = pygame.image.load("Graph.png")
        gameWin.blit(imageGraph,(100,100))
        show_text("PRESS BACKSPACE TO GO BACK",white,200,550,50)
        pygame.display.update()

# defining function to plot the graph
def plotGraph(LeaderBoard,UserName,UserScore):
    # getting the values for x and y axes
    x_value =[x[0] for x in LeaderBoard] 
    y_value = [int(x[1]) for x in LeaderBoard]
    x_value.append(UserName)
    y_value.append(int(UserScore))
    # plotting the graph
    plt.bar(x_value,y_value,color=['pink','purple','green','blue','red','yellow'])
    # giving labels to axes
    plt.xlabel("Players")
    plt.ylabel("Scores")
    #giving title to graph
    plt.title("Comparision of top players with You")
    # saving the graph
    plt.savefig("Graph.png")
# writing a function to display text
def show_text(text,color_text,x,y,fontsize):
    # setting font
    font = pygame.font.SysFont(None,fontsize)
    #rendering the text
    shown_text = font.render(text,True,color_text)
    # updates the window to display text
    gameWin.blit(shown_text,[x,y])
# defining function to display last screen
def EndScreen(scr):
    # getting all the scores from another function
    topScores,allScores = CheckData()
    # checking for quit game event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # writing score and name to the file
            with open("score.txt","a") as file:
                file.write(user + "," + str(scr) + "\n")
            pygame.quit() # quitting game
            quit()
        if event.type == pygame.KEYDOWN:
            # checking for process to play again
            if event.key == pygame.K_RETURN:
                # writing score to file
                with open("score.txt","a") as file:
                    file.write(user + "," + str(scr) + "\n")
                    # going back to game or restarting the game
                gameLoop()
            # checking event for diplaying graph screen
            if event.key == pygame.K_p:
                plotGraph(topScores,user,scr)
                displayGraph(scr)
    # changing format of screen
    gameWin.fill(yellow)
    font = pygame.font.SysFont(None,30)
    show_text("LEADERBOARD",red,300,50,50)
    name_y = 100
    # displaying the leaderboard
    for x in topScores:
        show_text(x[0],blue,320,name_y,30)
        show_text(str(x[1]),blue,450,name_y,30)
        name_y+= 30
    # finding current position in leaderboard
    your_pos =len(allScores)
    for x in allScores:
        if scr>int(x[1]) and allScores.index((x[0],x[1]))<your_pos:
            your_pos = allScores.index(x) + 1
            show_text("Congratulations!! You are now at position "+ str(your_pos),purple,200,270,30)
    text1 = "GAME OVER " 
    text3 = user + " your Score is :" +str (scr)
    textShow = font.render(text1,True,black)
    gameWin.blit(textShow,[350,300])
    show_text(text3,black,320,340,30)
    text2 = "PRESS ENTER TO PLAY AGAIN"
    textShow = font.render(text2,True,black)
    gameWin.blit(textShow,[300,380])
    show_text("Press P to see Plot",red,330,420,30)
    pygame.display.update()
    
        
    
# Creating the Game Loop
def gameLoop():
    # setting default position of bar 
    bar_x = 400
    # getting the image
    imageBar = pygame.image.load('bar.png')
    # seting velocity of bar
    vel_x = 0
    # game variables
    gameOver = False # variable to keep track of how long the game runs
    gameExit = False # variable to keep track of exiting the game
    # setting Score
    score = 0
    #giving cordinates to ball
    obs_x = random.randint(100,700)
    obs_y = 0
    # getting ball image
    ballImage = pygame.image.load('obstacle.png')
    # keep going till you exit game
    while not gameExit:
        if gameOver:
            # after game is over go to leaderboard screen
            EndScreen(score)
        else:
            # getting all the events happening
            for event in pygame.event.get():
                # checking for event to quit the game 
                if event.type == pygame.QUIT:
                    gameOver = True
                #cheking for right and left keystrokes
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_RIGHT:
                        vel_x = 30
                    if event.key == pygame.K_LEFT:
                        vel_x = -30
            # checking if the ball has been catched
            if obs_x in range(bar_x,(imageBar.get_width()+ bar_x)) and abs(obs_y - 550)<=20:
                score += 1  # updating score
                # giving new random position to ball
                obs_x = random.randint(100,700)
                obs_y = 0
           # giving speed to ball to fall towards the bar
            obs_y += 30
            # cheking if the bar has gone out of screen
            if bar_x <= -imageBar.get_width() or bar_x>=900:
                 gameOver = True
        # checking for missed ball
            if obs_y > 550 and not(obs_x in range(bar_x,(imageBar.get_width()+ bar_x)) and abs(obs_y - 550)<=20):
                 gameOver = True
            # setting screen format
            gameWin.fill(black)
            # displaying score
            show_text("SCORE: " + str(score) , white,0,0,50)
            # loading image of bar
            gameWin.blit(imageBar,(bar_x,550))
            # loading image of ball
            gameWin.blit(ballImage,(obs_x,obs_y))
            #updating position of bar
            bar_x += vel_x
            # updating the game display        
            pygame.display.update()
            # writing how many frames are displayed every second
            clock.tick(10)

# defining function to represent the introductory screen
def introScreen():
    global gameWin 
    # creating game display
    gameWin = pygame.display.set_mode((900,600))
    # setting title to the window
    pygame.display.set_caption("CATCH THE BALL")
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # checking condition to start the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
        # fornatting the screen
        gameWin.fill(black)
        show_text("Welcome to the game.",green ,350,250,30)
        show_text("Hope you enjoy the game",green,340,290,30)
        show_text("Press Enter to Begin",green,350,330,30)
        show_text("Your Goal is to prevent the ball from falling down",white,300,420,20)
        show_text("Use the left and right arrow keys to move the bar",white,310,440,20)
        pygame.display.update()
        clock.tick(10)
# function to accept user's name
def setting_user():
    # getting the name of the player
    global user 
    user = name.get()
    window.destroy()
    introScreen()
# function to create main window
def mainScreen():
    # creating main window
    global window 
    window = tk.Tk()
    # setting dimentions
    window.geometry("600x300")
    # giving title
    window.title("CATCH THE BALL")
    window['bg'] = 'black'
    # adding blanl spaces
    tk.Label(window,text="",bg="black").pack()
    tk.Label(window,text="",bg="black").pack()
    # displaying usernsme label
    tk.Label(window,text= "UserName").pack()
    # blank space
    tk.Label(window,text="",bg="black").pack()
    # accepting name of user
    global name 
    name= tk.Entry(window)
    name.pack()
    tk.Label(window,text="",bg="black").pack()
    # creating submit button to submit name
    tk.Button(window,text= "Submit",command = setting_user).pack()
    window.mainloop()
mainScreen()