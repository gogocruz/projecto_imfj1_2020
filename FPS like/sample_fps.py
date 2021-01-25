"""FPS-like application"""

#libraries used
import time
import random
import math
import pygame
import numpy

#imports from other files done
from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3, dot_product, cross_product
from quaternion import Quaternion


#function to create random cubes of differents sizes and colors
class RandomCube(Object3d):
    def __init__(self):
        super().__init__("RandomCube")
        #defining random height
        height = random.uniform(1,3)
        # Create a cube on a random positions
        self.mesh = Mesh.create_cube((random.uniform(0, 2), height,random.uniform(0, 2)))
        self.position = Vector3(random.uniform(-20, 20), (height / 2) -1, random.uniform(-20, 20))
                                #distance right and left      height       distance front and back

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

    # Specify the rotation of the object. It will rotate 15 degrees around the axis given, every second
    axis = scene.camera.up()
    axis.normalize()

    # Timer
    delta_time = 0
    prev_time = time.time()

    # Show mouse cursor
    pygame.mouse.set_visible(False)
    # Don't lock the mouse cursor to the game window
    pygame.event.set_grab(True)
    
    #Clean count to make a max nuber of cubes
    count = 0
    #Number of cubes in scene
    while count < 72:
        #function to add 72 cubes in scene at random
        new_cube = RandomCube()
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
                axis.normalize() 
        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0, 0, 20))

        keys=pygame.key.get_pressed()
        # Confine the mouse to the center of the screen         
        pygame.mouse.set_pos(res_x/2, res_y/2)        

        # Get the mouse movement from the last frmae
        rel = pygame.mouse.get_rel()

        # Gets the rotation angle
        rotAngle = rel[0] * 4

        if rel[0] != 0:
            # Rotates the object, considering the time passed (not linked to frame rate)
            q = Quaternion.AngleAxis(axis, math.radians(rotAngle) * delta_time)
            
            #camera rotation
            scene.camera.rotation = q * scene.camera.rotation
    
        ''' Movement Stuff'''
        
        #going forwards
        if keys[pygame.K_w]:
            scene.camera.position += scene.camera.forward() * delta_time * 4
        #going backwards
        if keys[pygame.K_s]:
            scene.camera.position -= scene.camera.forward() * delta_time * 4
        #going left
        if keys[pygame.K_a]:
            scene.camera.position -= scene.camera.right() * delta_time * 4
        #going right
        if keys[pygame.K_d]:
            scene.camera.position += scene.camera.right() * delta_time * 4
            
        # Render scene
        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        #Limit fps to 144
        while time.time() - prev_time < 0.00694:
            continue

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

# Run the main function
main()
