# lstsq_lm

##### Least Squares with Levenberg-Marquardt algorithm

Intended to be a class usable for fitting a data series to a function

In order to run the program you don't need to have installed nothing, this is a standalone Python class (you only need numpy) unlike other methods of LeastSquares like the Numerical Recipes in C one, much better but difficult to setup and use.

The class LeastSquares has a constructor LeastSquares(X, Y, f=None, P=None, w=None, dP=None, pr=False), the arguments are:
 - X is the independient variable, you can add dimensions as you want, use a list or a numpy array to define it, for example if you want x,y,z you must define [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]] (you can see it in examples 002 and 003)
 - Y is the dependient variable, you can add dimensions as you want, use a list of a numpy array to define it at the same way of X, for now there is no interesting example to do, so there is no examples
 - f is the function you want to fit, MUST HAVE 2 ARGUMENTS, x that is a item of your X array, and P as your parameter list, sometimes you must be tricky to define it
 - P is your parameter guess, try to define it because even if is a bad start, probably will be better than the class does (a list of 1e-3 parameters), if you don't define it, the program will start easily because it detects automatically the number of parameters you need
 - w is the weight function, is similar to f, with the requirements of x and P and is used for concentrate the fit in different parts of the curves (robust fit), you can see it in the example 003
 - dP is the typical variation of the parameter that you think the program have to use, the algorithm uses a non-dimensional damping so is not much important to define, but in strange fits can be important (I don't have a good and simple example to show you, because most of the time if you want to use it, you must have a difficult problem to solve)
 - pr is used for printing on the terminal

remember that you need to say to the solver that you want to solve it now, use the public method .solve() without arguments to do so.

I hope you find this simple Levenberg-Marquardt least squares solver useful. This is the result of the fits:

Linear regression 1D:

![Example001](https://github.com/hasbornasu/pylib/blob/master/lstsq_lm/examples_output/example_001.png)

Nonlinear modelation 1D: 

![Example002](https://github.com/hasbornasu/pylib/blob/master/lstsq_lm/examples_output/example_002.png)

Linear regression 2D:

![Example003](https://github.com/hasbornasu/pylib/blob/master/lstsq_lm/examples_output/example_003.png)

Nonlinear modelation 2D (family of curves, robust):

![Example004](https://github.com/hasbornasu/pylib/blob/master/lstsq_lm/examples_output/example_004.png)
