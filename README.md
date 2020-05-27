Eric Chen
Period 5

For the final project, I wanted to try a technique used to speed up render times called checkerboard rendering. It renders every other pixel, and fills the missing ones with a reconstruction filter. 
Checkerboard rendering is also used to upscale images to 4k. I am curious to see how much more efficient it would be compared to the current graphics engine. 
[Here is the paper that I am planning on basing my algorithm on]

#Features

Shading:
- Phong shading model

Antialiasing:
- Super sampling    

Reconstruction techniques:
- Nearest neighbor interpolation
- Linear interpolation 
- Bilinear interpolation (If time permits) 
- Bicubic interpolation  (If timer permits)


![Standard Rendering](https://abload.de/img/standard22hju1.png)
![Checkerboard Rendering](https://abload.de/img/checkerboard228joo.png)