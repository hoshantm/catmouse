#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:49:56 2019

@author: tarik
"""

# import the pygame module, so you can use it
import pygame
from pygame import time
import math
from pygame import gfxdraw
import catmouse

FRAME_RATE = 1000

SCREEN_SIZE = 650
MARGIN = 100
RADIUS = (SCREEN_SIZE - MARGIN) // 2
CENTER_X = SCREEN_SIZE // 2
CENTER_Y = SCREEN_SIZE // 2
    
CAT_RADIUS = 5
MOUSE_RADIUS = CAT_RADIUS
CAT_COLOR = (255, 0, 0)
MOUSE_COLOR = (0, 255, 0)
CIRCLE_COLOR = (255, 255, 255)
    
CAT_VELOCITY = 2.0
VELOCITY_RATIO = 4
MOUSE_VELOCITY = CAT_VELOCITY / VELOCITY_RATIO

DISTANCE_TOLERANCE = 5E-3

# define a main function
def main():

    catmouse.CAT_TO_MOUSE_SPEED_RATIO = VELOCITY_RATIO
     
    # initialize the pygame module
    pygame.init()
       
    #load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    
    pygame.display.set_caption("Cat Mouse")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    
    clock = pygame.time.Clock()
        
    cat_position = 0   
    mouse_position = (0.0, 0.0)
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
          
        
        cat_direction = get_cat_move(cat_position, mouse_position, VELOCITY_RATIO)        
        mouse_direction = get_mouse_move(cat_position, mouse_position, VELOCITY_RATIO)

        cat_position = get_updated_cat_position(clock, cat_direction, cat_position)
        mouse_position = get_updated_mouse_position(clock, mouse_position, mouse_direction)
        
        draw_circle(screen)
        draw_cat(screen, cat_position)
        draw_mouse(screen, mouse_position)
        
        if mouse_caught(cat_position, mouse_position, DISTANCE_TOLERANCE):
            print('Cat wins')
            running = False
        elif mouse_escaped(mouse_position):
            print('Mouse wins')
            running = False
        
        pygame.display.flip()

        clock.tick(FRAME_RATE)    
        
def get_updated_cat_position(clock, cat_direction, cat_position):
    cat_position += cat_direction * CAT_VELOCITY * clock.get_time() / 1000.0
    two_pi = 2 * math.pi
    if cat_position > two_pi:
        cat_position -= two_pi
    elif cat_position < 0:
        cat_position += two_pi
        
    return cat_position

def get_updated_mouse_position(clock, mouse_position, mouse_direction):
    x = mouse_position[0]
    y = mouse_position[1]
    v_x = mouse_direction[0]
    v_y = mouse_direction[1]
    x += v_x * MOUSE_VELOCITY * clock.get_time() / 1000.0
    y += v_y * MOUSE_VELOCITY * clock.get_time() / 1000.0
    return (x, y)
            
def draw_circle(screen):
    screen.fill((0, 0, 0))
    pygame.gfxdraw.aacircle(screen, CENTER_X, CENTER_Y, RADIUS, CIRCLE_COLOR)
        
def cat_position_to_screen_coordinates(cat_position):
    cat_x = int(CENTER_X + RADIUS * math.cos(cat_position))
    cat_y = int(CENTER_Y + RADIUS * math.sin(cat_position))
    return (cat_x, cat_y)

def mouse_position_to_screen_coordinates(mouse_position):
    x = mouse_position[0]
    y = mouse_position[1]
    screen_x = int(CENTER_X + RADIUS * x)
    screen_y = int(CENTER_Y + RADIUS * y)
    return (screen_x, screen_y)

def screen_coordinates_to_mouse_position(screen_coordinates):
    screen_x = screen_coordinates[0]
    screen_y = screen_coordinates[1]
    x = (screen_x - CENTER_X) / RADIUS
    y = (screen_y - CENTER_Y) / RADIUS
    return (x, y)
        
def draw_cat(screen, cat_position):
    cat_x, cat_y = cat_position_to_screen_coordinates(cat_position)
    pygame.gfxdraw.filled_circle(screen, cat_x, cat_y, CAT_RADIUS, CAT_COLOR)
    
def draw_mouse(screen, mouse_position):
    screen_x, screen_y = mouse_position_to_screen_coordinates(mouse_position)
    pygame.gfxdraw.filled_circle(screen, screen_x, screen_y, MOUSE_RADIUS, MOUSE_COLOR)
              
def get_mouse_move_human(cat_position, mouse_position, velocity_ratio):
    screen_x, screen_y = pygame.mouse.get_pos()
    pointer_x, pointer_y = screen_coordinates_to_mouse_position((screen_x, screen_y))
    mouse_x = mouse_position[0]
    mouse_y = mouse_position[1]
    distance = math.sqrt((pointer_x - mouse_x) ** 2 + (pointer_y - mouse_y) ** 2)
    if distance < DISTANCE_TOLERANCE:
        return (0, 0)
    v_x = (pointer_x - mouse_x) / distance
    v_y = (pointer_y - mouse_y) / distance
    return (v_x, v_y)

def get_cat_move(cat_position, mouse_position, velocity_ratio):
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        return -1
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        return 1
    elif pygame.key.get_mods() & pygame.KMOD_CAPS or pygame.key.get_pressed()[pygame.K_DOWN]:
        return 0

    mouse_x = mouse_position[0]
    mouse_y = mouse_position[1]
    if (mouse_x == 0 and mouse_y == 0):
        return 0
    
    mouse_angle = math.atan2(mouse_y, mouse_x)
    if mouse_angle < 0:
        mouse_angle += 2 * math.pi
            
    if abs(mouse_angle - cat_position) < DISTANCE_TOLERANCE:
        cat_move = 0
    else:
        diff = mouse_angle - cat_position
        if diff < 0:
            diff += 2 * math.pi
        if 0 < diff < math.pi:
            cat_move = 1
        else:
            cat_move = -1
    
    return cat_move

def mouse_caught(cat_position, mouse_position, distance_tolerance):
    cat_x = math.cos(cat_position)
    cat_y = math.sin(cat_position)
    mouse_x = mouse_position[0]
    mouse_y = mouse_position[1]
    
    distance2 = (cat_x - mouse_x) ** 2 + (cat_y - mouse_y) ** 2
    return distance2 <= distance_tolerance ** 2

def mouse_escaped(mouse_position):
    mouse_x = mouse_position[0]
    mouse_y = mouse_position[1]
    
    return mouse_x ** 2 + mouse_y ** 2 >= 1    

class mouse_auto:
    def __init__(self):
        self.phase = 0

    def get_move(self, cat_position, mouse_position, velocity_ratio):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        mouse_r = math.sqrt(mouse_x ** 2 + mouse_y ** 2)
        mouse_angle = math.atan2(mouse_y, mouse_x)
        if mouse_angle < 0:
            mouse_angle += 2 * math.pi

        '''
        Phase 0: Progress from the center to a radius of
        1 / velocity_ratio while staying on a diametrically
        oposite angle from the cat. This is possible within
        the circle of radius of 1 / velocity_ratio because the
        angular velocity of the mouse can be keep up with the
        angular velocity of the cat.
        ''' 
        if self.phase == 0:
            # Angle diametrically opposite to the cat
            target_angle = cat_position + math.pi
            if target_angle > 2 * math.pi:
                target_angle -= 2 * math.pi

            # If the mouse is equal to the target angle within a small tolerance
            if abs(target_angle - mouse_angle) < DISTANCE_TOLERANCE:
                # Continue progressing outward until 1 / velocity_ratio is reached
                if mouse_r < 1 / velocity_ratio - DISTANCE_TOLERANCE:
                    v_x = math.cos(mouse_angle)
                    v_y = math.sin(mouse_angle)
                    return (v_x, v_y)
                # 1 / velocity_ratio has been passed, backtrack a bit
                elif mouse_r > 1 / velocity_ratio:
                    v_x = -math.cos(mouse_angle)
                    v_y = -math.sin(mouse_angle)
                    return (v_x, v_y)
                # All is well, the mouse has gone as far as possible outward
                # while staying diametrically opposite the cat. It's now time
                # to dash towards the outer rim.
                else:
                    self.phase = 1
                    return (0, 0)
            # Mouse is not diametrically opposit the cat
            else:
                # Determine if it is falling behind or is ahead.
                diff = target_angle - mouse_angle
                if diff < 0:
                    diff += 2 * math.pi
                if 0 < diff < math.pi:
                    angle_direction = 1
                else:
                    angle_direction = -1

                # If the mouse has not reached the distance of 1 / velocity_ratio,
                # continue progressing but also move in a tangent to keep up with
                # the cat and stay diametrically opposite.
                if mouse_r < 1 / velocity_ratio - DISTANCE_TOLERANCE:
                    v_r = math.sqrt(1/velocity_ratio ** 2 - mouse_r ** 2)
                    v_t = math.sqrt(1 - v_r ** 2)
                    v_x = math.cos(mouse_angle) * v_r + angle_direction * math.cos(mouse_angle + math.pi / 2) * v_t
                    v_y = math.sin(mouse_angle) * v_r + angle_direction * math.sin(mouse_angle + math.pi / 2) * v_t
                    return (v_x, v_y)
                # If the mouse has passed 1 / velocity_ratio, backtrack. Otherwise
                # the mouse will not be able to keep up with the cat in terms of rotation.
                elif mouse_r > 1 / velocity_ratio:
                    v_x = -math.cos(mouse_angle)
                    v_y = -math.sin(mouse_angle)
                    return (v_x, v_y)
                # The mouse is close to the edge of the circle with radius 1 / velocity_ratio
                # Keep rotating to ensure the mouse is diametrically opposite the cat within an
                # acceptable tolerance.
                else:
                    v_x = angle_direction * math.cos(mouse_angle + math.pi / 2)
                    v_y = angle_direction * math.sin(mouse_angle + math.pi / 2)
                    return (v_x, v_y)
        # The mouse has progressed a far as it could while staying diametrically
        # opposite the cat. It is now time to progress towards the outer rim
        # in such a way that no matter what the cat does (what direction it takes)
        # it will not be able to get to the mouse on time.
        else:
            mouse_angle = mouse_angle - cat_position
            if mouse_angle < 0:
                mouse_angle += 2 * math.pi

            escape_angle = catmouse.maxDiffTimeCatMouse(mouse_r, mouse_angle)[0]
            escape_angle = escape_angle + cat_position
            if escape_angle > 2 * math.pi:
                escape_angle -= 2 * math.pi

            v_x = math.cos(escape_angle)
            v_y = math.sin(escape_angle)
            return (v_x, v_y)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    print('The cat cat be fully controlled by having caps ON and using the left and right arrow. Having the caps OFF, you can stop the cat movement by pressing the down arrow.')
    mouse_user = input('Input \'a\' if you want the computer to control the mouse, press enter otherwise: ')
    if mouse_user == 'a':
        get_mouse_move = mouse_auto().get_move
    else:
        get_mouse_move = get_mouse_move_human

    str_velocity_ratio = input('Input cat to mouse velocity ratio (0.1 to 10) or press enter to keep the default of 4: ')
    try:
        VELOCITY_RATIO = float(str_velocity_ratio)
        if VELOCITY_RATIO < 0.1:
            VELOCITY_RATIO = 0.1
        elif VELOCITY_RATIO > 10:
            VELOCITY_RATIO = 10
        MOUSE_VELOCITY = CAT_VELOCITY / VELOCITY_RATIO
    except:
        pass

    # call the main function
    main()
    pygame.quit()
    input('Press any key to exit')
