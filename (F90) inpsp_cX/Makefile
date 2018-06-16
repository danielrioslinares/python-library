

# This target compiles all the files in the directory
compile: inpsp_cX.f90
	f2py -m -c inpsp_cX_f90 inpsp_cX.f90

# This target generates the python modules
module: inpsp_cX.f90
	f2py inpsp_cX.f90 -m inpsp_cX_f90 -h inpsp_cX_f90.pyf

# This target removes all libraries created
clean:
	rm *.so ; rm -rf __pycache__ ; rm *.pyf
