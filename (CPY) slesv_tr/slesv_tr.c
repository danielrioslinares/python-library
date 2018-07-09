/* slesv_tr.c */

/* Standard bool (C99) */
#include <stdbool.h>

/* Python C API */
#include <Python.h>


// <function slesv_tr(PyObject* list)>
// 	@argument <PyObject* list1> : input Python list 1 (C API)
// 	@argument <PyObject* list2> : input Python list 2 (C API)
// 	@argument <PyObject* list2> : input Python list 3 (C API)
//
//	@returns <PyObject* list> : output Python list (C API)
//
// 	@description : Python list treatment of 1 input list with 1 new output list
//
//	@name : input_3x_PyList1D__output_1x_PyList1D
//		    |     |  |       |      |  |
//		    |     |  |       |      |  PyList
//		    |     |  |       |      1
//		    |     |  |       returns
//		    |     |  PyList
//		    |     3
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 9, 2017
//
PyObject* slesv_tr(PyObject* list1, PyObject* list2, PyObject* list3, PyObject* list4) {

	/* Check list size */
	int N = PyList_Size(list1);

	/* Declare arrays */
	double Aupp[N];
	double Adia[N];
	double Alow[N];
	double B[N];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++)
		Aupp[i] = PyFloat_AsDouble(PyList_GetItem(list1, (Py_ssize_t) i));
	for (int i = 0 ; i < N ; i++)
		Adia[i] = PyFloat_AsDouble(PyList_GetItem(list2, (Py_ssize_t) i));
	for (int i = 0 ; i < N ; i++)
		Alow[i] = PyFloat_AsDouble(PyList_GetItem(list3, (Py_ssize_t) i));
	for (int i = 0 ; i < N ; i++)
		B[i] = PyFloat_AsDouble(PyList_GetItem(list4, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double X[N];

	/* Temporal arrays */
	double P[N];
	double Q[N];

	// Alow[0] and Aupp[-1] are 0 (this must be met)
	Alow[0] = 0;
	Aupp[N-1] = 0;

	// P[0] and Q[0] are known because Alow[0] = 0 always
	P[0] = - Aupp[0] / Adia[0];
	Q[0] = B[0] / Adia[0];

	// Obtain temporal vectors of gaussian elimination
	for (int i = 1 ; i < N ; i++) {
		P[i] = - Aupp[i] / (Adia[i] + Alow[i] * P[i-1]);
		Q[i] = (B[i] - Alow[i] * Q[i-1]) / (Adia[i] + Alow[i] * P[i-1]);
	}

	// X[-1] is known because Aupp[-1] = 0 -> P[-1] = 0
	X[N-1] = Q[N-1];

	// X[i] is obtainable from X[-1]
	for (int i = N-2 ; i >= 0 ; i--)
		X[i] = P[i] * X[i+1] + Q[i];

	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* result = PyList_New(N);

    for (int i = 0; i < N; i++)
    	PyList_SetItem(result, i, PyFloat_FromDouble(X[i]));
	/* End of Python list fill */

    return result;
}
