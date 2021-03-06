# fractal
This repo features a CLI app implementing the fractal drawing process via two algorithms - escapetime and DEM. Images will be generated in the newly created `img` folder.

## CLI app usage
Implementation is in the file `fractal.py`. It allows you to draw two types of fractals - Julia sets and the Mandelbrot set. 
It accepts multiple arguments that help with fractal image creation. Two examples:

```bash
python fractal.py julia "1 0 -0.760+0.0698j" 
-px 2000 -it 500 -cm cubehelix_r -cmp 0.8 -ext .png
```
```bash
fractal.py mandelbrot
-px 2000 -cmp 0.7 -fn mandelbrot_img -ext .jpg --cache
```

### CLI arguments
- **type:** The first argument is either `julia` or `mandelbrot` depending on which type of fractal you want to draw.
- **polynomial:** If you chose `julia` as the first argument, then you must also specify the associated polynomial. Those are formatted as strings, e.g. `"1 2 3"` means the polynomial `1*z^2 + 2*z + 3`.
- **center:** This is the center around which the image is focused. It defaults to 0 and is set by e.g. `-c "1 + 0.5j"`.
- **radius:** This is the radius around the center, set by e.g. `-r 2`. If center is 0, then the radius can be calculated algorithmically. Else, you have to specify it.
- **algorithm:** You can choose the algorithm used for drawing a chosen fractal as `-alg` following by either `escapetime` or `DEM` (Distance estimation method). The default is `DEM`.
- **iterations:** This is the number of iterations that approximate convergance, used by the chosen algorithm. This can be set by `-it` following by some positive integer. The default is `1000`.
- **pixels:** This is the square root of the number of pixels of the generated square image. Set by `-px` followed by positive integer. Default is `1000`.
- **colormap:** You can specify the colormap by adding `-cm` followed by some `matplotlib` colormap name. The default for julia sets is `inferno`, while for the mandelbrot set it's `gist_stern_r`. You can check the available options [here](https://matplotlib.org/stable/tutorials/colors/colormaps.html) or `import cm from matplotlib` and doing `dir(cm)`.
- **invert colormap:** You can color the set interior with the outermost colour (defined by the chosen colormap) by typing `-ic` followed by either `continuous` or `inverted`. Default is `continuous`, but `inverted` is appropriate when using escapetime, so the interior is dark like the area far from the set. In this way the bright border is better visible.
- **colormap power:** Sometimes the border is thin and barely visible, because all iteration values returned by the algorithm are either very close to 0 or very close to 1. This can be fixed by applying roots or powers. It can be done by e.g. `-cmp 2`, which  squares all values before applying the colormap. So, it brings numbers close to 1 lower and out of hiding.
- **colormap percentage power:** This is a generalization of colormap power. Powering all the values by the same power may bring those close to 1 lower as well as those already close to 0. This is fixed by differentating the powers applied to some high and low values, which are specified by the given percentage. Use as e.g. `-cpc 91 4 0.25`. See examples for more.
- **file name:** To set the filename of the file use `-fn`. By default files are saved by the command that generated them (trust me, that's a good idea!).
- **extension:** To set the image type, set `-ext` followed by some extension. Default is `.png`.
- **cache:** Drawing a fractal image can take a lot of time, so you might save the general fractal-related info by adding `--cache` to your command. Then you can test different colorings without having to again generate the fractal itself. Whenever you have cached data available (in the `data` folder) for a chosen command, the program recognized this and uses that cached data. The data can be reused if the generating command used the same **type**, **algorithm**, **center**, **radius**, **pixels** and **iterations**.

### Examples
To understand `-cpc` command see the following examples:
```bash
python fractal.py julia "1 0 -0.7510894579318156+0.11771693494277351j" 
-cm cubehelix
```
```bash
python fractal.py julia "1 0 -0.7510894579318156+0.11771693494277351j" 
-cm cubehelix -cpc 91 4 0.25
```
```bash
python fractal.py julia "1 0 0.1567002004882749+0.6527033090669409j" 
-cm magma -it 1000 -cpc 85 2 0.25
```