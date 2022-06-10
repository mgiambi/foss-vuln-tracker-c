import subprocess
import os
from src.definitions import LHDIFF_PATH

from src.ldiff_wrapper.diff_range import DiffRange

class Diff:

    def __init__(self):
        pass

    def make_diff(self, left_file, right_file):
    	return_list = []

    	pipe = subprocess.Popen(["java", "-jar", LHDIFF_PATH, left_file, right_file], universal_newlines=True, stdout=subprocess.PIPE)
    	result, err = pipe.communicate()
    	result = result.splitlines()
    	result.pop(0)

    	for line in result:
    		diff = line.split(",")
    		return_list.append((diff[0], diff[1]))

    	return DiffRange(return_list)





