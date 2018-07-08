/* arr_siso.c */

/* Standard bool (C99) */
#include <stdbool.h>

/* Python C API */
#include <Python.h>

// <function input_1x_PyList1D__output_1x_PyList1D(PyObject* list)>
// 	@argument <PyObject* list> : input Python list (C API)
//
//	@returns <PyObject* list> : output Python list (C API)
//
// 	@description : Python list treatment of 1 input list with 1 new output list
//
//	@name : input_1x_PyList1D__output_1x_PyList1D
//		    |     |  |     |   |      |  |     |
//		    |     |  |     |   |      |  |     1D
//		    |     |  |     |   |      |  PyList
//		    |     |  |     |   |      1
//		    |     |  |     |   returns
//		    |     |  |     1D
//		    |     |  PyList
//		    |     1
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_1x_PyList1D__output_1x_PyList1D(PyObject* list) {

	/* Check list size */
	int N = PyList_Size(list);

	/* Declare array */
	double array[N];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++)
		array[i] = PyFloat_AsDouble(PyList_GetItem(list, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output[N];



	// Do what you wanna do, for example, duplicate all values in the input list
	for (int i = 0 ; i < N ; i++)
		output[i] = array[i] * 2;




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* result = PyList_New(N);

    for (int i = 0; i < N; i++)
    	PyList_SetItem(result, i, PyFloat_FromDouble(output[i]));
	/* End of Python list fill */

    return result;
}

// <function input_1x_PyList2D__output_1x_PyList2D(PyObject* list)>
// 	@argument <PyObject* list> : input Python 2D list (C API)
//
//	@returns <PyObject* list> : output Python 2D list (C API)
//
// 	@description : Python list treatment of 1 input list with 1 new output list
//
//	@name : input_1x_PyList2D__output_1x_PyList2D
//		    |     |  |     |   |      |  |     |
//		    |     |  |     |   |      |  |     2D
//		    |     |  |     |   |      |  PyList
//		    |     |  |     |   |      1
//		    |     |  |     |   returns
//		    |     |  |     2D
//		    |     |  PyList
//		    |     1
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_1x_PyList2D__output_1x_PyList2D(PyObject* list) {

	/* Check list size */
	int N = PyList_Size(list);
	int M = PyList_Size(PyList_GetItem(list, 0));

	/* Declare array */
	double array[N][M];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++) {
		for (int j = 0 ; j < M ; j++)
			array[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(list, i), j));

	}
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output[N][M];



	// Do what you wanna do, for example, duplicate all values in the input list
	for (int i = 0 ; i < N ; i++) {
		for (int j = 0 ; j < M ; j++)
			output[i][j] = 2 * array[i][j];
	}





	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* result = PyList_New(N);
	for (int i = 0 ; i < N ; i++) {
		PyObject* result_i = PyList_New(M);
		for (int j = 0 ; j < M ; j++)
			PyList_SetItem(result_i, j, PyFloat_FromDouble(output[i][j]));
		PyList_SetItem(result, i, result_i);
	}
	/* End of Python list fill */

    return result;
}
