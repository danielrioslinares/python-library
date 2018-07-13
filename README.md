# python-library
This is a library of Python 3 implementations made by myself in order to practise numerical algorithms, this modules are intended to show a good approach to the problem as simple as possible without fancies detections (in general). There are three different possible implementations: Standalone Python 3 denoted by (PYT), Python 3 C API (CPY) and Python-Fortran wrapper (F90).

- arr_XiYo : CPY only, a C API wrapper for Python 3 that allows to parse PyList to C arrays, do the treatment and return. Templates. It consists on 4 modules depending of number of inputs and outputs
  - arr_siso : SISO, Single Input Single Output. Only one list as input, only one list  as output.
  - arr_simo : SIMO, Single Input Multiple Output. Only one list as input, more than one lists as output.
  - arr_miso : MISO, Multiple Input Single Output. More than one lists as input, only one list as output.
  - arr_mimo : MIMO, Multiple Input Multiple Output. More than one lists as input, more than one lists as output.
- intsm_ue : Simpson integration method for a non-uniform mesh of 1D set of data X,Y.
- inttp_ue : Trapezoidal integration method for a non-uniform mesh of 1D set of data X,Y.
- mxinv_gj : Matrix inversion using Gauss-Jordan pivoting algorithm. Pass the square matrix A as argument to return A⁻¹.
- rtf1d_mu : Root Finding 1D class storing f(x) function to root and optionally dfdx(x) for Newton-Raphson, then calling the different methods (bisection, secant, regulafalsi, ridders, brent, newtonraphson) returns the x0 which f(x0)=0.
- slesv_tr : system of linear equations solver for tridiagonal matrix of coefficients.
- slesv_pt : system of linear equations solver for pentadiagonal matrix of coefficients.
- inpsp_cX : Interpolation with cubic splines
- bvp2o1d1euei_fd1 : BVP (Boundary Value Problem) solver for second order differential equations of the form y'' = f(y,x) (no y' term).
- bvp2o1d1euec_diffusion : BVP (Boundary Value Problem) solver for second order differential equations - d/dx ( D(x) * dy/dx ) + K(x) y(x) = q(x), diffusion equation.
