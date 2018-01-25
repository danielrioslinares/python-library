

# This target compiles all the files in the directory
compile: mxinv_gj.f90
	f2py -m -c mxinv_gj_f90 mxinv_gj.f90

# This target generates the python modules
module: mxinv_gj.f90
	f2py mxinv_gj.f90 -m mxinv_gj_f90 -h mxinv_gj_f90.pyf

# This target removes all libraries created
clean:
	rm *.so ; rm -rf __pycache__ ; rm *.pyf
