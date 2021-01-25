"""Sphere sample application"""
import time
import math
import pygame
import numpy
import sys

from quaternion import Quaternion

from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3

# Define a main function, just to keep things nice and tidy
def main():
    """Main function, it implements the application loop"""
    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 640
    res_y = 480

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("TestScene")
    scene.camera = Camera(False, res_x, res_y)

    # Moves the camera back 2 units
    scene.camera.position -= Vector3(0, 0, 4)

    # Create a sphere and place it in a scene, at position (0,0,0)
    '''
    obj1 = Object3d("TestObject")
    obj1.scale = Vector3(1, 1, 1)
    obj1.position = Vector3(0, 0, 0)
    obj1.mesh = Mesh.create_sphere((1, 1, 1), 12, 12)
    obj1.material = Material(Color(1, 0, 0, 1), "TestMaterial1")
    scene.add_object(obj1)
    '''
    # puts name of file that you wanna load
    # if you dont want to load a file leave it as ""
    fileloaded = "teste2.obj"

    #if theres so file to be loaded
    if fileloaded == "":
        # Create a pyramid and place it in a scene, at position (0,0,0)
        obj1 = Object3d("TestObject")
        obj1.scale = Vector3(1, 1, 1)
        obj1.position = Vector3(0, 0, 0)
        obj1.mesh = Mesh.create_pyramid()
        obj1.material = Material(Color(1, 0, 0, 1), "TestMaterial1")
        scene.add_object(obj1)
    
    else:
        # Create a object chosen by the user and place it in a scene, at position (0,0,0)
        obj1 = Object3d("TestObject")
        obj1.scale = Vector3(1, 1, 1)
        obj1.position = Vector3(0, 0, 0)
        
        #function to enable objects to be loaded from terminal
        if len(sys.argv) == 2:
            print(True)
            obj1.mesh = Mesh.create_mesh(sys.argv[1])
        #if nothing at the terminal just run normaly with the name of the file in code
        else:    
            obj1.mesh = Mesh.create_mesh(fileloaded)
        # add object to viewer
        obj1.material = Material(Color(1, 0, 0, 1), "TestMaterial1")
        scene.add_object(obj1)

    # Specify the rotation of the object. It will rotate 15 degrees around the axis given,
    # every second
    angle = 50
    axis = Vector3(1, 0.7, 0.2)
    axis.normalize()

    # Timer
    delta_time = 0
    prev_time = time.time()

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)

    # Game loop, runs forever
    while True:
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if event.type == pygame.QUIT:
                # Exits the application immediately
                return
            #if your pressing a key
            elif event.type == pygame.KEYDOWN:
                #exit the game
                if event.key == pygame.K_ESCAPE:
                    return
                # rotate object in y axis
                if event.key == pygame.K_LEFT:
                    axis = Vector3(0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    axis = Vector3(0,-1,0)
                # rotate object in x axis
                if event.key == pygame.K_UP:
                    axis = Vector3(1, 0, 0)
                if event.key == pygame.K_DOWN:
                    axis = Vector3(-1, 0, 0)
                # rotate object in z axis
                if event.key == pygame.K_PAGEUP:
                    axis = Vector3(0, 0, 1)
                if event.key == pygame.K_PAGEDOWN:
                    axis = Vector3(0, 0, -1)
                #normalize axis
                axis.normalize()

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0, 0, 0))

        # Rotates the object, considering the time passed (not linked to frame rate)
        ax = (axis * math.radians(angle) * delta_time)

        q = Quaternion.AngleAxis(axis, math.radians(angle) * delta_time)
        

        #Object movement
        keys=pygame.key.get_pressed()
        # movementing object up down right and left
        if keys[pygame.K_LEFT]:
            obj1.rotation = q * obj1.rotation 
        if keys[pygame.K_RIGHT]:
            obj1.rotation = q * obj1.rotation 
        if keys[pygame.K_UP]:
            obj1.rotation = q * obj1.rotation 
        if keys[pygame.K_DOWN]:
            obj1.rotation = q * obj1.rotation 
            
        #functions to make the rotations work
        if keys[pygame.K_PAGEUP]:
            obj1.rotation = q * obj1.rotation
        if keys[pygame.K_PAGEDOWN]:
            obj1.rotation = q * obj1.rotation
        if keys[pygame.K_w]:
            obj1.position = Vector3(obj1.position.x,obj1.position.y+0.006,obj1.position.z)
        if keys[pygame.K_s]:
            obj1.position = Vector3(obj1.position.x,obj1.position.y-0.006,obj1.position.z)    
        if keys[pygame.K_a]:
            obj1.position = Vector3(obj1.position.x-0.006,obj1.position.y,obj1.position.z)
        if keys[pygame.K_d]:
            obj1.position = Vector3(obj1.position.x+0.006,obj1.position.y,obj1.position.z)
        if keys[pygame.K_q]:
            obj1.position = Vector3(obj1.position.x,obj1.position.y,obj1.position.z-0.006) 
        if keys[pygame.K_e]:
            obj1.position = Vector3(obj1.position.x,obj1.position.y,obj1.position.z+0.006) 
        
        #rendering objects on to screen
        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()


# Run the main function
main()
