# Test and create new method to generate exp_vec

import random

exp_vec = [10*random.random() for i in range(75)]

# A variant on the above, to correct for outliers
def generate_exp_lvl_vec2(exp_vec, K):
	# Outputs a list of size exp_vec where each value
	# has been converted to a value in [1,..., K]
	sorted_indices = [i[0] for i in sorted(enumerate(exp_vec), key=lambda x:x[1])]
	lvl_vec = [K-1 for x in range(len(exp_vec))]
	cutoffs = [i*int(float(len(exp_vec) / K)) for i in range(K)]
	print cutoffs
	for k in range(len(cutoffs) - 1):
		for ind in range(cutoffs[k],cutoffs[k+1]):
			lvl_vec[sorted_indices[ind]] = k
	return lvl_vec


print exp_vec
print generate_exp_lvl_vec2(exp_vec, 3)