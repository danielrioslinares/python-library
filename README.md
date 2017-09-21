# python-libraries
A collection of all python implementations made by myself, in order to practise Python and numerical algorithms, this modules are intended to show a good approach to the problem as simple as possible:

- intsm_ue : Simpson integration method for a non-uniform mesh of 1D set of data X,Y. In order to use it you have to import the method intsm_ue from intsm_ue module and simply pass X,Y as argument.
- inttp_ue : Trapezoidal integration method for a non-uniform mesh of 1D set of data X,Y. In order to use it you have to import the method inttp_ue from inttp_ue module and simply pass X,Y as argument.
- lstsq_lm : Least Squares using Levenberg-Marquardt algorithm, multidimensional, family of curves and robust fit of a set of data X,Y to a function Y = f(X), the module has got a class named LeastSquares(X,Y,f), consult the examples.
- mxinv_gj : Matrix inversion using Gauss-Jordan pivoting algorithm. In order to use it you have to import the method mxinv_gj from mxinv_gj module and simply pass the square matrix A as argument to return A⁻¹.
- rtf1d_mu : Root Finding 1D class storing f(x) function to root and optionally dfdx(x) for Newton-Raphson, then calling the different methods (bisection, secant, regulafalsi, ridders, brent, newtonraphson) returns the x0 which f(x0)=0. WARNING: YOU MAY NEED F2PY TO WORK WITH IT
