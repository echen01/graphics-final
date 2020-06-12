## Eric Chen
## Period 5


### MDL Features
- Light\  Sets a point light\  ``` light symbol x y z r g b```
- Shading\ Sets shading model (flat, gouraud, phong, raytrace)\ ``` shading shading_type ```
- Plane (Only works in raytrace mode)\ Creates an infinite 2D plane\ ``` plane x y z x_normal y_normal z_normal ```

### Shading Features
- Flat shading
- Gouraud shading
- Phong shading
- Ray tracing

### Notes
- Objects on to be ray traced must be placed on a 2x2 grid from (-1, -1) to (1, 1) instead of the 500x500 grid. This is due to how the pinhole camera model works. I couldn't get it to work on the 500x500 grid. 
- Ray traced polygons become invisible or glitch out sometimes. 
- I spent so much time debugging my ray tracing code that I had to abandon my original plan to create antialiasing and upscaling algorithms. 
