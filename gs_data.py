# gs_data.py (Generate Simulated Data)
# Generates simulated paired haplotype and expressiond data


# Input Format:
# >> python gs_data.py [# haplotypes] [length of haplotype] [expression_fn] [noise] [name of output file]

# Options for [expression_fn]
# rand: randomly generated expression values (ie. no pattern-specific expression)

# [noise]: a value [0, 1] determining the level of noise added to the expression_fn


# Output Files Format
# A file where every line is of the format:
# haplotype \t expression value 

import sys
import random 

# Parse command line arguments
try:
	num_haps = int(sys.argv[1])
	hap_len = int(sys.argv[2])
	exp_fn_name = sys.argv[3]
	noise = float(sys.argv[4])
	output_file_path = sys.argv[5]
except:
	print "ERROR: improper input argument format"
	print "Correct Format:"
	print ">> python gs_data.py [# haplotypes] [length of haplotype] [expression_fn] [noise] [name of output file]"

# Open the output file
f = open(output_file_path, 'w')

### Define Expression Functions ###
# Which function is called is based on command line argument
def random_fn(input_hap, noise):
	return random.random()


# Choose the specified expression function
if exp_fn_name == 'rand':
	exp_fn = random_fn
else:
	exp_fn = random_fn

# Write to the output file
for i in range(num_haps):
	hap_str = ''.join(str(x)[0] for x in [round(random.random()) for k in range(hap_len)])
	exp_val = str(exp_fn(hap_str, noise))
	f.write(hap_str + '\t' + exp_val + '\n')

# Close the output file
f.close()




