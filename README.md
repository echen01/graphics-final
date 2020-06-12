## Eric Chen
## Period 5


### MDL Features
- Light
<br/>Sets a point light
<br/>``` light symbol x y z r g b```
<br/>
- Shading
<br/>Sets shading model (flat, gouraud, phong, raytrace)
<br/>``` shading shading_type ```
<br/>
- Plane (Only works in raytrace mode)
<br/>Creates an infinite 2D plane
<br/>``` plane x y z x_normal y_normal z_normal ```

### Shading Features
- Flat shading
- Gouraud shading
- Phong shading
- Ray tracing

### Notes
- Objects on to be ray traced must be placed on a 2x2 grid from (-1, -1) to (1, 1) instead of the 500x500 grid. This is due to how the pinhole camera model works. I couldn't get it to work on the 500x500 grid. 
- Ray traced polygons become invisible or glitch out sometimes. 
- I spent so much time debugging my ray tracing code that I had to abandon my original plan to create antialiasing and upscaling algorithms. 
