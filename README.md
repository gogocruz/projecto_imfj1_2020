# Introdução à Matemática e Física Para Videojogos I - Final Project

## Group members:
|Name | Student Number | GitHub Account |
| ----|----------------|--------------- |
|Daniel Pinhão| 22007445 | https://github.com/DanielPinhao22007445 |
|Diogo Cruz   | 22008318 | https://github.com/gogocruz|
|Ritik Joshi  | 22002818 | https://github.com/ritikjoshi24 |
 
### Individual Contributions!
#####  Viewer Aplication
#
    -> Daniel Pinhão - Created a 3d model for display, a n-sided pyramid and a model loaded from a file. 
    -> Diogo Cruz - Corrected the model loaded froma a file and fixed some visualisation bugs
>Extra -> Added the possibility to load the model files from the terminal (Ex. py sample_viewer.py trex.obj)

#####  Fps Like
#
    -> Ritick Joshi added the first movimentation with some bugs
    -> Daniel made the enviroment 
    -> Diogo Cruz corrected the bugs from the player movement, camera movement on the y axis and other boring bugs and added the "Stop objects that are behind the camera from being renderered"
    
## Problems and solutions
#####  Viewer Aplication
#
    -> We had a problem loading the two last triangles on the rectangular loaded modules, and to fix it we made a program append the faces ('f') two times, one from the begining of the line and the other from the end of the line.

#####  Fps Like
#
    -> We had a lot of trouble making the mouse movements for all directions so we choose to dont use the z axis so the player cant look up or down.
