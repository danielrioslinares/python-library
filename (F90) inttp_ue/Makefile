

# This target compiles all the files in the directory
compile: inttp_ue.f90
	f2py -m -c inttp_ue_f90 inttp_ue.f90

# This target generates the python modules
module: inttp_ue.f90
	f2py inttp_ue.f90 -m inttp_ue_f90 -h inttp_ue_f90.pyf

# This target removes all libraries created
clean:
	rm *.so ; rm -rf __pycache__ ; rm *.pyf
