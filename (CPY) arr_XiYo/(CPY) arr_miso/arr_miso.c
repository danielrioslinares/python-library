/* arr_miso.c */

/* Standard bool (C99) */
#include <stdbool.h>

/* Python C API */
#include <Python.h>


// <function input_2x_PyList1D__output_1x_PyList1D(PyObject* list)>
// 	@argument <PyObject* list1> : input Python list 1 (C API)
// 	@argument <PyObject* list2> : input Python list 2 (C API)
//
//	@returns <PyObject* list> : output Python list (C API)
//
// 	@description : Python list treatment of 1 input list with 1 new output list
//
//	@name : input_2x_PyList1D__output_1x_PyList1D
//		    |     |  |       |      |  |
//		    |     |  |       |      |  PyList
//		    |     |  |       |      1
//		    |     |  |       returns
//		    |     |  PyList
//		    |     2
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_2x_PyList1D__output_1x_PyList1D(PyObject* list1, PyObject* list2) {

	/* Check if list is a PyList_Type */
	if (!PyList_Check(list1)) return NULL;
	if (!PyList_Check(list2)) return NULL;

	/* Check list size */
	int N1 = PyList_Size(list1);
	int N2 = PyList_Size(list2);

	/* Declare arrays */
	double array1[N1];
	double array2[N2];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N1 ; i++)
		array1[i] = PyFloat_AsDouble(PyList_GetItem(list1, (Py_ssize_t) i));
	for (int i = 0 ; i < N2 ; i++)
		array2[i] = PyFloat_AsDouble(PyList_GetItem(list2, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output[N1];

	// Do what you wanna do, for example, dot multiplication
	for (int i = 0 ; i < N1 ; i++)
		output[i] = array1[i] * array2[i];




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* result = PyList_New(N1);

    for (int i = 0; i < N1; i++)
    	PyList_SetItem(result, i, PyFloat_FromDouble(output[i]));
	/* End of Python list fill */

    return result;
}

// <function input_3x_PyList1D__output_1x_PyList1D(PyObject* list)>
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
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_3x_PyList1D__output_1x_PyList1D(PyObject* list1, PyObject* list2, PyObject* list3) {

	/* Check if list is a PyList_Type */
	if (!PyList_Check(list1)) return NULL;
	if (!PyList_Check(list2)) return NULL;
	if (!PyList_Check(list3)) return NULL;

	/* Check list size */
	int N1 = PyList_Size(list1);
	int N2 = PyList_Size(list2);
	int N3 = PyList_Size(list3);

	/* Declare arrays */
	double array1[N1];
	double array2[N2];
	double array3[N3];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N1 ; i++)
		array1[i] = PyFloat_AsDouble(PyList_GetItem(list1, (Py_ssize_t) i));
	for (int i = 0 ; i < N2 ; i++)
		array2[i] = PyFloat_AsDouble(PyList_GetItem(list2, (Py_ssize_t) i));
	for (int i = 0 ; i < N3 ; i++)
		array3[i] = PyFloat_AsDouble(PyList_GetItem(list3, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output[N1];

	// Do what you wanna do, for example, dot multiplication
	for (int i = 0 ; i < N1 ; i++)
		output[i] = array1[i] * array2[i] * array3[i];




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* result = PyList_New(N1);

    for (int i = 0; i < N1; i++)
    	PyList_SetItem(result, i, PyFloat_FromDouble(output[i]));
	/* End of Python list fill */

    return result;
}

// <function input_3x_PyList1D__output_1x_PyList1D(PyObject* list)>
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
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_4x_PyList1D__output_1x_PyList1D(PyObject* list1, PyObject* list2, PyObject* list3, PyObject* list4) {

	/* Check if list is a PyList_Type */
	if (!PyList_Check(list1)) return NULL;
	if (!PyList_Check(list2)) return NULL;
	if (!PyList_Check(list3)) return NULL;
	if (!PyList_Check(list4)) return NULL;

	/* Check list size */
	int N1 = PyList_Size(list1);
	int N2 = PyList_Size(list2);
	int N3 = PyList_Size(list3);
	int N4 = PyList_Size(list4);


	/* Declare arrays */
	double array1[N1];
	double array2[N2];
	double array3[N3];
	double array4[N4];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N1 ; i++)
		array1[i] = PyFloat_AsDouble(PyList_GetItem(list1, (Py_ssize_t) i));
	for (int i = 0 ; i < N2 ; i++)
		array2[i] = PyFloat_AsDouble(PyList_GetItem(list2, (Py_ssize_t) i));
	for (int i = 0 ; i < N3 ; i++)
		array3[i] = PyFloat_AsDouble(PyList_GetItem(list3, (Py_ssize_t) i));
	for (int i = 0 ; i < N4 ; i++)
		array4[i] = PyFloat_AsDouble(PyList_GetItem(list4, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output[N1];

	// Do what you wanna do, for example, dot multiplication
	for (int i = 0 ; i < N1 ; i++)
		output[i] = array1[i] * array2[i] * array3[i] * array4[i];




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* result = PyList_New(N1);

    for (int i = 0; i < N1; i++)
    	PyList_SetItem(result, i, PyFloat_FromDouble(output[i]));
	/* End of Python list fill */

    return result;
}
