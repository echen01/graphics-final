## Eric Chen
## Period 5

# Proposal 
For the final project, I wanted to try a technique used to speed up render times called checkerboard rendering. It renders every other pixel, and fills the missing ones with a reconstruction filter. 
Checkerboard rendering is also used to upscale images to 4k. I am curious to see how much more efficient it would be compared to the current graphics engine. 
[Here is the paper that I am planning to base my algorithm on](https://pdfs.semanticscholar.org/56b3/fd1f33aeaf901ca4686b7860b2d0b7e554a6.pdf?_ga=2.150886710.1298991178.1590542660-1340839336.1589332552).

# Features

### Shading:
- Wireframe
- Flat shading
- Gouraud shading
- Phong shading

### Antialiasing:
- Super sampling    

### Reconstruction techniques:
- Nearest neighbor interpolation
- Linear interpolation 
- Bilinear interpolation (If time permits) 
- Bicubic interpolation (If time permits)


# A diagram explaining the algorithm
![Standard Rendering](https://abload.de/img/standard22hju1.png)
![Checkerboard Rendering](https://abload.de/img/checkerboard228joo.png)