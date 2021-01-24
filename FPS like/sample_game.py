"""Game sample application"""

import time
import random
import math
import pygame

from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3, dot_product, cross_product
from quaternion import Quaternion
from perlin import noise2d

class RandomCube(Object3d):
    def __init__(self, mesh):
        super().__init__("RandomCube")
        # Create a cube on a random positions
        self.position = Vector3(random.uniform(-30, 30), random.uniform(0, 0), random.uniform(-30, 30))
                            #distance right and left         height?          distance front and back
        self.mesh = mesh
        # Pick a random Color for the cube
        self.material = Material(Color(random.uniform(0.1, 1),
                                       random.uniform(0.1, 1),
                                       random.uniform(0.1, 1), 1),
                                 "CubeMaterial")

def main():
    """Main function, it implements the application loop"""

    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 1280
    res_y = 720

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("TestScene")
    scene.camera = Camera(False, res_x, res_y)
    # Moves the camera back 2 units
    scene.camera.position -= Vector3(0, 0, 0)


    # Specify the rotation of the object. It will rotate 15 degrees around the axis given,
    # every second
    angle = 50
    axis = Vector3(1, 0.7, 0.2)
    axis.normalize()

    # Timer
    delta_time = 0
    prev_time = time.time()

    # Show mouse cursor
    pygame.mouse.set_visible(True)
    # Don't lock the mouse cursor to the game window
    pygame.event.set_grab(False)

    count = 0
    while count < 20:
        cube_mesh = Mesh.create_cube(((random.uniform(0, 2)), (random.uniform(0, 2)), (random.uniform(0, 2))))
                                                      # cubes size
        new_cube = RandomCube(cube_mesh)
        scene.add_object(new_cube)
        count += 1


    # Game loop, runs forever
    while True:

        # Process OS events
        for event in pygame.event.get():
            
            # Checks if the user closed the window
            if event.type == pygame.QUIT:
                # Exits the application immediately
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RIGHT:
                    axis = Vector3(0, 2, 0)
                if event.key == pygame.K_LEFT:
                    axis = Vector3(0,-2,0)
                if event.key == pygame.K_DOWN:
                    axis = Vector3(2, 0, 0)
                if event.key == pygame.K_UP:
                    axis = Vector3(-2, 0, 0)
                axis.normalize() 

             # Rotates the object, considering the time passed (not linked to frame rate)
            ax = (axis * math.radians(angle) * delta_time)

            q = Quaternion.AngleAxis(axis, math.radians(angle) * delta_time)

            keys=pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                scene.camera.rotation = q * scene.camera.rotation 
            if keys[pygame.K_LEFT]:
                scene.camera.rotation = q * scene.camera.rotation 
            if keys[pygame.K_DOWN]:
                scene.camera.rotation = q * scene.camera.rotation 
            if keys[pygame.K_UP]:
                scene.camera.rotation = q * scene.camera.rotation 
            if keys[pygame.K_s]:
                scene.camera.position -= Vector3(0, 0, .08)
            if keys[pygame.K_w]:
                scene.camera.position += Vector3(0, 0, .08)
            if keys[pygame.K_a]:
                scene.camera.position -= Vector3(0.2, 0, 0)
            if keys[pygame.K_d]:
                scene.camera.position += Vector3(0.2, 0, 0)
            
          
        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0, 0, 0))

        # Render scene
        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

# Run the main function
main()
