

// <function intsm_ue(X, Y)>
// 	@argument <double[] X> : 1D array with all the input independient variable
// 	@argument <double[] Y> : 1D array with all the f(X) of dependient variable
//
//	@returns <double out> : integration of f(x) along X
//
// 	@description : implementation of the Simpson integration for a non-uniform
//		1D mesh
//
//	@example: integration of f(x) = x^2 in the interval x = [0,1]
//		X = [i/100 for i in range(101)]
//		Y = [x**2 for x in X]
//		result = intsm_ue(X,Y)
//
//	@name : intsm_ue
//		    |  |  |
//		    |  |  non-uniform grid
//		    |  gration method
//		    Integration
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 5, 2017
//
double intsm_ue(int N, double* X, int M, double* Y) {

	double out = 0;
	double s;
	int mid = (int) N / 2 + 1;
	int n;
	double x_nm1,x_np0,x_np1;
	double h[11];

	for (int j = 1 ; j < mid ; j++) {
		n = 2 * j - 1;

		// If N is even, is required a trapezoidal approximation at final:
		if (n + 1 >= N)
			break;

		// X[n-1], X[n], X[n+1]
		x_nm1 = X[n-1];
		x_np0 = X[n];
		x_np1 = X[n+1];

		// Increments h
		h[0] = x_np1    + x_np0;
		h[1] = x_np1    + x_nm1;
		h[2] = x_np0    + x_nm1;
		h[3] = x_np1    - x_nm1;
		h[4] = x_np1    - x_np0;
		h[5] = x_np0    - x_nm1;
		h[6] = x_np1    * x_np0;
		h[7] = x_np1    * x_nm1;
		h[8] = x_np0    * x_nm1;
		h[9] = x_np1 * x_np1 - x_nm1 * x_nm1;
		h[10] = x_np1 * x_np1 * x_nm1 - x_nm1 * x_nm1 * x_nm1;

		// Simpson's method
		s = 0;
		s += Y[n-1] * h[4] * ( h[10]/3 - h[0] * h[9]/2 + h[6] * h[3] );
		s -= Y[n  ] * h[3] * ( h[10]/3 - h[1] * h[9]/2 + h[7] * h[3] );
		s += Y[n+1] * h[5] * ( h[10]/3 - h[2] * h[9]/2 + h[8] * h[3] );
		out += s / ( h[4] * h[3] * h[5] );

	}

	if (N % 2 == 0)
		out -= ( X[N-2] - X[N-1] ) * ( Y[N-1] + Y[N-2] ) / 2;

	return out;
}
