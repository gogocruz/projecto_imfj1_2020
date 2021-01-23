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

class Missile(Object3d):
    """Missile class.
    The missile will launch from a random position (defined on instancing) and will direct itself
    towards the player.
    """
    missile_mesh = None
    """Mesh used by all the missiles, so we don't create a new one every single missile"""
    missile_material = None
    """Material used by all the missiles, so we don't create a new one every single missile"""

    def __init__(self):
        if Missile.missile_mesh is None:
            Missile.missile_mesh = Missile.create_missile_mesh()
            Missile.missile_material = Material(Color(1, 0, 0, 1), "MissileMaterial")

        super().__init__("Missile")

        # Determine the spawn position. There's 33% chance it comes from the right, 33% that it
        # comes from behind the mountains, and 34% chance it comes from the left
        self.position = Vector3(0, random.uniform(0, 3), 12)
        r = random.uniform(0, 100)
        if r > 66:
            self.position.x = 7
            self.rotation = Quaternion.AngleAxis(Vector3(0, 1, 0), math.radians(-90))
        elif r > 33:
            self.position.y = -2
            self.position.x = random.uniform(-4, 4)
            self.rotation = Quaternion.AngleAxis(Vector3(1, 0, 0), math.radians(-90))
        else:
            self.position.x = -7
            self.rotation = Quaternion.AngleAxis(Vector3(0, 1, 0), math.radians(90))

        # Set the mesh and material of the missile
        self.mesh = Missile.missile_mesh
        self.material = Missile.missile_material
        # Sets the missile linear speed
        self.missile_speed = 2
        # Sets the rotation speed (in radians per second)
        self.missile_rotation_speed = 0.75

    def update(self, delta_time):
        """Animates the missile."""
        # Moves missile based on its direction (the forward vector)
        velocity = self.forward() * self.missile_speed
        self.position += velocity * delta_time

        # Rotate missile towards the player - Figure out where it is pointing and
        # where do we want to point it
        current_dir = self.forward()
        desired_dir = (Vector3(0, 0, 0) - self.position).normalized()
        # Find the angle between these two directions
        dp = max(-1, min(1, dot_product(current_dir, desired_dir)))
        angle = math.acos(dp)

        # If the angle is larger than the ammount we can rotate a single frame,
        # given by the time elapsed and the missile rotation speed, we need to
        # clamp the value of the angle
        if abs(angle) > self.missile_rotation_speed * delta_time:
            angle = self.missile_rotation_speed * delta_time * math.copysign(1, angle)

        # Figure out the rotation axis to point the missile towards the desired direction
        axis = cross_product(current_dir, desired_dir)
        axis.normalize()

        if (angle > 0.01):
            # Rotate the missile towards the player
            q = Quaternion.AngleAxis(axis, angle)
            self.rotation = q * self.rotation

    @staticmethod
   

    def __init__(self):
        

        # The position and direction will be overwritten by the code that spawns the shot
        self.position = Vector3(0, 0, 0)
        self.mesh = Shot.shot_mesh
        self.material = Shot.shot_material
        self.shot_speed = 6
        self.direction = Vector3(0, 0, 0)

    def update(self, delta_time):
        """Animates the missile."""
        # Moves the shot in the direction set
        velocity = self.direction * self.shot_speed
        self.position += velocity * delta_time

# Computes the height of the terrain at the given x,y point
def sample_height(x, y):
    """Samples a pseudo heighmap, built with 2-octaves of 2d perlin noise. This is
    clamped near the player, so we have a nice flat area near him. We also clamp it to
    values above 0, so it looks more natural"""
    # 2 octave noise, with a given scale
    scale_noise = 0.4
    noise_height = 5
    n = 0.5 * noise2d(x * scale_noise, y * scale_noise)
    n += 0.25 * noise2d(x * scale_noise * 2, y * scale_noise * 2)
    n *= noise_height
    if ((n < 0) or (y < 8)):
        n = 0

    return n

def create_terrain():
    """Creates a terrain to use as a background in the game"""
    # Size of the terrain
    size_x = 30
    size_z = 30
    # Number of divisions of the terrain. Vertex count scales with the square of this
    div = 20

    px = size_x / div
    pz = size_z / div

    # For centering the terrain on the object center
    origin = Vector3(-size_x * 0.5, 0, 0)

    terrain_mesh = Mesh("Terrain")

    # Create the geometry of the terrain and add it to the mesh
    for dz in range(0, div):
        for dx in range(0, div):
            p1 = Vector3(dx * px, 0, dz * pz) + origin
            p2 = Vector3((dx + 1) * px, 0, dz * pz) + origin
            p3 = Vector3((dx + 1) * px, 0, (dz + 1) * pz) + origin
            p4 = Vector3(dx * px, 0, (dz + 1) * pz) + origin

            p1.y = sample_height(p1.x, p1.z)
            p2.y = sample_height(p2.x, p2.z)
            p3.y = sample_height(p3.x, p3.z)
            p4.y = sample_height(p4.x, p4.z)

            poly = []
            poly.append(p1)
            poly.append(p2)
            poly.append(p3)
            poly.append(p4)

            terrain_mesh.polygons.append(poly)

    # Create materials for the terrain
    terrain_material = Material(Color(0.1, 0.6, 0.1, 1), "TerrainMaterial")

    # Create object to display the terrain
    obj = Object3d("TerrainObject")
    obj.scale = Vector3(1, 1, 1)
    obj.position = Vector3(0, -1, 1)
    obj.mesh = terrain_mesh
    obj.material = terrain_material

    return obj

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

    # Creates the terrain meshes and materials
    terrain_object = create_terrain()
    scene.add_object(terrain_object)

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
                if event.key == pygame.K_PAGEUP:
                    axis = Vector3(0, 0, 2)
                if event.key == pygame.K_PAGEDOWN:
                    axis = Vector3(0, 0, -2)
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
            if keys[pygame.K_PAGEUP]:
                scene.camera.rotation = q * scene.camera.rotation
            if keys[pygame.K_PAGEDOWN]:
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
