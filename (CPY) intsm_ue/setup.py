
import instant
import numpy as np
import os

# Read function
c_code = open('intsm_ue.c', 'r').read()

# Create module
instant.build.build_module(modulename = "intsm_ue_c",
	code = c_code,
	arrays = [['N','X'],['M','Y']],
	include_dirs = [np.get_include()],
	system_headers = ['numpy/arrayobject.h'],
	init_code = 'import_array();'
	)

# Test it
from intsm_ue_c import intsm_ue

a = intsm_ue(np.array([1.0,2.0,3.0,4.0,5.0]),np.array([1.0,1.0,1.0,1.0,1.0]))

print("The result must be 4.0 ->",a)
