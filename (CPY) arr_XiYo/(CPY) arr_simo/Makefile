



# Libraries required
PYT_LIB := $(shell pkg-config --cflags --libs python3)
LOC_LIB := $(shell pwd)
NPY_LIB := $(shell python -c "import numpy ; print(str(numpy.get_include()))")


# Create the wrappers and compile the library
compile:
	# arr_simo library
	swig -python -debug-tmsearch arr_simo.i ; rm arr_simo.py ; sed -i 's/_arr_simo/arr_simo/g' arr_simo_wrap.c
	gcc -fPIC -shared arr_simo.c arr_simo_wrap.c $(PYT_LIB) -o arr_simo.so

# Clean the directory
clean:
	rm -r *.o ; rm -r *.out ; rm -rf __pycache__ ; rm *.so

# Test
test:
	python -c "import arr_simo ; print(arr_simo.input_1x_PyList1D__output_2x_PyList1D([1,2,3])) ; print(arr_simo.input_1x_PyList1D__output_3x_PyList1D([1,2,3])) ; print(arr_simo.input_1x_PyList1D__output_4x_PyList1D([1,2,3]))"
