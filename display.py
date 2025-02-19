# import the pygame module 
import pygame 
import CPU
# Define the background colour 
# using RGB color coding. 
background_colour = (0, 0, 0) 
cpu = CPU.CPU()
# Define the dimensions of 
# screen object(width,height) 
screen = pygame.display.set_mode((640, 320)) 
  
# Set the caption of the screen 
pygame.display.set_caption('Geeksforgeeks') 
  
# Fill the background colour to the screen 
screen.fill(background_colour) 
  
# Update the display using flip 
pygame.display.flip() 
  
# Variable to keep our game loop running 
running = True

displayMatrix = [[False for x in range(32)] for x in range(64)]

keymap = [120,49,50,51,113,119,101,97,115,100,122,99,52,114,102,118]
key = None
# game loop 
while running: 
    
    draw = cpu.CPUcycle(key)
    
    if draw:
        if draw == "clean":
            displayMatrix = [[False for x in range(32)] for x in range(64)]

        else:
            x,y = draw[0], draw[1]
            for data in draw[2]:
                for i in range(1,9):
                   
                    if x+i >= 64:
                        break
                    if y >= 32:
                        break
                    val = (data >> 8-i) & 1
                    if val == 1:
                        displayMatrix[x+i][y] = not displayMatrix[x+i][y]
                y+=1
                  
                        
      
    if draw:
        for i in range(64):
            for j in range(32):
                color = (255,255,255) if displayMatrix[i][j] == True else (0,0,0)
                pygame.draw.rect(screen,color, (i*10,j*10,i*10+10,j*10+10),0)

    pygame.display.update()

    for event in pygame.event.get(): 
      
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN:
            for i,item in enumerate(keymap):
                if item == event.key:
                    key = i
        elif event.type == pygame.KEYUP:
            if event.key == keymap[key]:
                key = None

            