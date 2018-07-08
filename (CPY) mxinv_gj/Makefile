



# Libraries required
PYT_LIB := $(shell pkg-config --cflags --libs python3)
LOC_LIB := $(shell pwd)


# Create the wrappers and compile the library
compile:
	# mxinv_gj library
	swig -python -debug-tmsearch mxinv_gj.i ; rm mxinv_gj.py ; sed -i 's/_mxinv_gj/mxinv_gj/g' mxinv_gj_wrap.c
	gcc -fPIC -shared mxinv_gj.c mxinv_gj_wrap.c $(PYT_LIB) -o mxinv_gj.so

# Clean the directory
clean:
	rm -r *.o ; rm -r *.out ; rm -rf __pycache__ ; rm *.so

# Test
test:
	python -c "import mxinv_gj ; print(mxinv_gj.mxinv_gj([[1,2],[3,4]]))"
