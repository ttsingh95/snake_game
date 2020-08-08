import curses
from random import randint

#setting up window
curses.initscr()
#create new  setup
win = curses.newwin(20,60,0,0) #20 lines (y-coordinate), 60 columns (x coordinate) starting @ 0,0
win.keypad(1) #use arrow keys to control snake
curses.noecho() #don't wanna listen to other input characters
curses.curs_set(0) #hide cursor
win.border(0) #draw border
win.nodelay(1) #not waiting for next user to hit key

#need data structure to keep track of snake and food
#(4,10), (4,9)... --> starting coordinates of snake. 4,10 = head; 4,8 = tail
#snake and food
snake = [(4,10),(4,9),(4,8)] #for snake - using list + tuple; tuple allows python to optimize better than lists
food = (10,20)


win.addch(food[0], food[1], '❖')
#game logic
score = 0

#this should keep running until user hits esc key
ESC = 27
key = curses.KEY_RIGHT #starting by moving the snake right

#while key is not equal to escape
while key != ESC:
    win.addstr(0,2,'Score '+ str(score) + ' ') #draw score in screen
    win.timeout(150-(len(snake)) // 5 + len(snake)//10 % 120 ) #formula to increase speed of snake when it gets bigger

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key #first key was right, now next key is this one

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_UP, ESC]:
        key = prev_key

    #calculate next coordinate for snake
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0,(y,x))

#If snake crosses the boundaries, game ends
    # if y == 0: break
    # if y == 19: break
    # if x ==0: break
    # if x ==59: break

#If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1

#if snake touches/runs over itself
    if snake[0] in snake[1:]:break

#check if snake eats food
    if snake[0]== food:
        score += 1 #score increases
        food = ()
        while food == ():
            food = (randint(1,18),randint(1,58))
            if food in snake:
                food = ()
        win.addch(food[0],food[1],'❖')

    else:  #move snake
        last = snake.pop()
        win.addch(last[0],last[1], ' ')

#for every coordinate- add character; c[0] --> y coordinate
    win.addch(snake[0][0], snake[0][1], '♦')



curses.endwin()
print(f"Final score = {score}")

#improving it:
#1. if you hit left arrow when it's facing right itll close -fix
#2. if you reach end of border, make it so it passes through and enters from other side