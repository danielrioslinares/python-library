

// <function inttp_ue(X, Y)>
// 	@argument <double[] X> : 1D array with all the input independient variable
// 	@argument <double[] Y> : 1D array with all the f(X) of dependient variable
//
//	@returns <double inte> : integration of f(x) along X
//
// 	@description : implementation of the trapezoidal integration for a
//		non-uniform 1D mesh
//
//	@example: integration of f(x) = x^2 in the interval x = [0,1]
//		X = [i/100 for i in range(101)]
//		Y = [x**2 for x in X]
//		result inttp_ue(X,Y)
//
//	@name : inttp_ue
//		    |  |  |
//		    |  |  non-uniform grid
//		    |  trapezoidal integration method
//		    Integration
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 5, 2018
//
double inttp_ue(int N, double* X, int M, double* Y) {

	double out = 0;

	for (int i = 1 ; i < N ; i++) {
		out = out + ( X[i] - X[i-1] ) * ( Y[i] + Y[i-1] ) / 2;
	}

	return out;
}
