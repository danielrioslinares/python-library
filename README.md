# python-library
This is a library of Python 3 implementations made by myself in order to practise numerical algorithms, this modules are intended to show a good approach to the problem as simple as possible without fancies detections (in general).

## python 3 standalone
A collection of all python standalone implementations:

- bvp2o1d1euei_fd1 : BVP (Boundary Value Problem) solver for second order differential equations of the form y'' = f(y,x) (no y' term).
- bvp2o1d1euec_diffusion : BVP (Boundary Value Problem) solver for second order differential equations - d/dx ( D(x) * dy/dx ) + K(x) y(x) = q(x), diffusion equation.
- intsm_ue : Simpson integration method for a non-uniform mesh of 1D set of data X,Y. In order to use it you have to import the method intsm_ue from intsm_ue module and simply pass X,Y as argument.
- inttp_ue : Trapezoidal integration method for a non-uniform mesh of 1D set of data X,Y. In order to use it you have to import the method inttp_ue from inttp_ue module and simply pass X,Y as argument.
- lstsq_lm : Least Squares using Levenberg-Marquardt algorithm, multidimensional, family of curves and robust fit of a set of data X,Y to a function Y = f(X), the module has got a class named LeastSquares(X,Y,f), consult the examples.
- mxinv_gj : Matrix inversion using Gauss-Jordan pivoting algorithm. In order to use it you have to import the method mxinv_gj from mxinv_gj module and simply pass the square matrix A as argument to return A⁻¹.


## F2PY version (python with fortran embedded)
A collection of fortran implementations with python wrapper, very useful for bigger arguments or when python is really slow, it uses F2PY application from numpy (in the makefiles you have access to the compile command):

- (F90) bvp2o1d1euei_fd1 : BVP (Boundary Value Problem) solver for second order differential equations of the form y'' = f(y,x) (no y' term).
- (F90) intsm_ue : Simpson integration method for a non-uniform mesh of 1D set of data X,Y. In order to use it you have to import the method intsm_ue from intsm_ue module and simply pass X,Y as argument.
- (F90) inttp_ue : Trapezoidal integration method for a non-uniform mesh of 1D set of data X,Y. In order to use it you have to import the method inttp_ue from inttp_ue module and simply pass X,Y as argument.
- (F90) mxinv_gj : Matrix inversion using Gauss-Jordan pivoting algorithm. In order to use it you have to import the method mxinv_gj from mxinv_gj module and simply pass the square matrix A as argument to return A⁻¹.
- (F90) rtf1d_mu : Root Finding 1D class storing f(x) function to root and optionally dfdx(x) for Newton-Raphson, then calling the different methods (bisection, secant, regulafalsi, ridders, brent, newtonraphson) returns the x0 which f(x0)=0.
