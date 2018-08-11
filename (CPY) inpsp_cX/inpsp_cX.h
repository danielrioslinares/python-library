/* array_simo.h */

/* Standard bool (C99) */
#include <stdbool.h>

/* Python C API */
#include <Python.h>

/* array_simo.c functions */
PyObject* inpsp_cs(
    // New mesh to interpolate
    PyObject* PyList_Xnew,
    // Known X vs Y
    PyObject* PyList_X,
    PyObject* PyList_Y,
    // Momentums, initial and final,typically will be both 0 (natural spline)
    PyObject* PyFloat_Mi,
    PyObject* PyFloat_Mf
    );

PyObject* inpsp_cf(
    // New mesh to interpolate
    PyObject* PyList_Xnew,
    // Known X vs Y
    PyObject* PyList_X,
    PyObject* PyList_Y,
    // Momentums, initial and final,typically will be both 0 (natural spline)
    PyObject* PyFloat_Ci,
    PyObject* PyFloat_Cf
	);
