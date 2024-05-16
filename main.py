import math
import random
import time
import pygame
pygame.init()

#window
WIDTH = 800 
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

BG_COLOR = (0, 25, 40) #dark blue
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24) #font object

LIVES = 3

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)


    while run:   
        clock.tick(60) #sets frame rate to 60 fps
        click = False  
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():  #quits window
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:   #generates random targets on screen
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)   
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)  
                target = Target(x, y)   
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:  #check if mouse interacted with target
                click = True
                clicks += 1

        for target in targets: #updates targets causing them to grow and shrink
            target.update()

            if target.size <= 0:  #removes target when they srink down, counts torwars a missed target
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos): #mouse - target interaction, counts torwars score
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES: #ends game
            end_sceen(WIN, elapsed_time, target_pressed, clicks)

        draw_targets(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()

    pygame.quit()


class Target: 
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    #Target grows then shrinks
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
    
    #draws a target with 5 circles alternating between red and white circles decreasing in size
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.2)

    def collide(self, x, y):  #mouse-target collision
        dist = math.sqrt((x - self.x)**2 + (y - self.y)**2)  #distance between two points
        return dist <= self.size


#Draws targets in window 
def draw_targets(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

    

#formats time to minutes, seconds and milliseconds
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}:{milli}"

#draws simple UI for game
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Seed: {speed} t/s", 1 , "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1 , "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1 , "black")

    win.blit(time_label, (5,5))
    win.blit(speed_label, (225,5))
    win.blit(hits_label, (450,5))
    win.blit(lives_label, (650,5))


#end game UI
def end_sceen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Seed: {speed} t/s", 1 , "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1 , "white")

    accuracy = round(targets_pressed / clicks * 100 , 1)
    acuuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1 , "white")

    win.blit(time_label, (get_middle(time_label),50))
    win.blit(speed_label, (get_middle(speed_label),100))
    win.blit(hits_label, (get_middle(hits_label),150))
    win.blit(acuuracy_label, (get_middle(acuuracy_label),200))

    #wais for user to press something to exit screen
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
            

#to center endscreen
def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2


main()