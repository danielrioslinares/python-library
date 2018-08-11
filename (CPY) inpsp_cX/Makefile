




# Libraries required
PYT_LIB := $(shell pkg-config --cflags --libs python3)
LOC_LIB := $(shell pwd)
NPY_LIB := $(shell python -c "import numpy ; print(str(numpy.get_include()))")


# Create the wrappers and compile the library
compile:
	# inpsp_cX library
	swig -python -debug-tmsearch inpsp_cX.i ; rm inpsp_cX.py ; sed -i 's/_inpsp_cX/inpsp_cX/g' inpsp_cX_wrap.c
	gcc -fPIC -shared inpsp_cX.c inpsp_cX_wrap.c $(PYT_LIB) -o inpsp_cX.so

# Clean the directory
clean:
	rm -r *.o ; rm -r *.out ; rm -rf __pycache__ ; rm *.so
