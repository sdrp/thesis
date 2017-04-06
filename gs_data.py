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
import numpy

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
	# Generate expression randomly between 0 and 10
	return random.random() * 10

def gaussian_fn(input_hap, noise):
	# Generates values from a Gausian distribution 
	# with parameters mu and sigma
	mu = 5 # mean
	sigma = 1 # standard deviation
	return max(0, numpy.random.normal(mu, sigma))


# Choose the specified expression function
tract_dependent = False
if exp_fn_name == 'rand':
	exp_fn = random_fn
elif exp_fn_name == 'sanity_check':
	exp_fn = sanity_check_fn
elif exp_fn_name == 'tract_dependent':
	tract_dependent = True
elif exp_fn_name == 'snp_dependent':
	exp_fn = snp_fn
elif exp_fn_name == 'gaussian':
	exp_fn = gaussian_fn
else:
	exp_fn = random_fn


# Generate random haps
haps = [[round(random.random()) for k in range(hap_len)] for x in range(num_haps)]
exp_vals = [0 for x in range(num_haps)]


if tract_dependent:
	# Generate the haps to have tract dependent expression
	# Define a number of classes we want to emulate
	K = 5
	# Determine a tract-associated expression boost
	tract_val = 10
	# Next determine a tract length
	tract_len = int((hap_len * 0.67) / K) # arbitrary proportion
	# Get tract start points
	tract_starts = [k*(hap_len/K) for k in range(K)]
	# Get generate the tract signatures (ie. the tracts themselves)
	tracts = [[round(random.random()) for i in range(tract_len)] for k in range(K)]
	# Now inject the tracts into the haplotypes
	for i in range(num_haps):
		# Pick a random expression level for this hap 
		exp_level = random.randint(0, K-1)
		# Place modify the hap to have the tract
		hap = haps[i]
		hap[tract_starts[exp_level]:tract_starts[exp_level]+tract_len] = tracts[exp_level]
		# Generate an expression value
		exp_vals[i] = (random.random()*10) + (exp_level*tract_val)
	# Write the tracts and expression to file
	for i in range(num_haps):
		hap = haps[i]
		hap_str = ''.join(str(x)[0] for x in hap)
		f.write(hap_str + '\t' + str(exp_vals[i]) + '\n')

else:
	# Write to the output file
	for i in range(num_haps):
		hap = haps[i]
		exp_val = exp_fn(hap, noise)
		hap_str = ''.join(str(x)[0] for x in hap)
		f.write(hap_str + '\t' + str(exp_val) + '\n')

# Close the output file
f.close()




