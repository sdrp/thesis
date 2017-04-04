# Tractus Tree Method for Predicting Expression


# Usage:  
# >> python tractus_tree.py [name of input file, in hap_exp format]

# 1) Simulates data based on input arguments 
# 2) Constructs a tractus tree from the simlated haplotypes
# 3) Trains a binary (eventually n-ary) classification algorithm based on common tracts

import sys
import numpy as np


### Classes ###
# Define a node in the suffix tree
class Node():
	def __init__(self):
		self.edges = [] # outgoing edges
		self.tags_on = [] # node defines the end of a suffix (ie. it is a leaf)
		self.tags_below = [] # all tags below the node
		self.tract_so_far = []	# the tract referred to by this node

	def is_leaf(self):
		# Determines if the nodes is a leaf (ie. no outgoing edges) 
		return self.edges == []

	def add_edge(self, edge):
		# Adds edge to given node
		self.edges.append(edge)

	def add_tag_below(self, tag):
		# Adds tag to list of tags below node
		self.tags_below.append(tag)

	def add_tag_on(self, tag):
		# Adds tag to list of tags below node
		self.tags_on.append(tag)

	def get_tags_below(self):
		# Return all unique tags below
		return list(set(self.tags_below))

	def get_tags_on(self):
		# Return all unique tags on
		return list(set(self.tags_on))

	def display(self):
		# Prints the node's fields to stdout, for visual output
		print "---TRACT---"
		print self.tract_so_far
		print "Tags On: %s" % str(self.get_tags_on())
		print "Tags Below: %s" % str(self.get_tags_below())
		if self.is_leaf():
			print "LEAF"
		else:
			print ">> Edges"
			for edge in self.edges:
				print ">" + str(edge.tract)
		print "\n" # Leave space after displaying

# Define an edge in the suffix tree
class Edge():
	def __init__(self, start_node, end_node, sub_tract):
		self.start_node = start_node
		self.end_node = end_node
		self.tract = sub_tract # a list of ints

### Helper Functions ###
def print_tractus_tree(root):
	# Outputs a description of the tree given by root to stdout
	# Uses DFS and Node.display()
	root.display()
	for edge in root.edges:
		print_tractus_tree(edge.end_node)

def tractize(input_hap):
	# Converts input_hap (a binary vector) into tractized form
	return [(2*j)+input_hap[j] for j in range(len(input_hap))]

def common_prefix(s1, s2):
	# Finds the longest common prefix of two input lists
	# Returns the index that defines that substring such that:
	# s1[0:pref_ind] = s2[0:pref_ind] 
	# pref_ind = 0 when input vectors have no common prefix
	last_ind = min(len(s1), len(s2))
	for i in range(last_ind):
		if s1[i] != s2[i]:
			return i
	return last_ind

def insert(root, suff, tag_val):
	# Inserts suff (a list of ints) into Tractus tree given by root
	def add_suff_to_root():
		# Simply adds suff as new edge off root
		leaf = Node()
		leaf.add_tag_on(tag_val) # this leaf defines unique suffix
		root.add_tag_below(tag_val) # now tag_val is below root
		leaf.tract_so_far = root.tract_so_far + suff
		new_edge = Edge(root, leaf, suff)
		root.add_edge(new_edge)
		return root

	if suff == "":
		# Suffix is empty string, nothing to insert
		return root 
	elif root.edges == []:
		# Root has no edges, we simply add the entire suffix to the root
		return add_suff_to_root()
	else:
		# Root has edges
		common_pref_found = False
		for edge in root.edges:
			pref = common_prefix(suff, edge.tract)
			if pref != 0:
				# There is a common prefix 
				common_pref_found = True
				if (pref == len(edge.tract)) and (pref == len(suff)):
					# the shared prefix is this entire edge
					root.add_tag_below(tag_val)
					edge.end_node.add_tag_on(tag_val)
					return root
				elif (pref == len(edge.tract)) and (pref < len(suff)):
					# The suffix is longer than the shared prefix
					# We take the additional part of the suffix and insert it below
					root.add_tag_below(tag_val)
					rest_of_suff = suff[pref:]
					edge.end_node = insert(edge.end_node, rest_of_suff, tag_val)
					return root
				elif (pref < len(edge.tract)) and (pref == len(suff)):
					# The edge is longer than the suffix
					# Create a new mid-point edge
					first_part = edge.tract[0:pref]
					last_part = edge.tract[pref:]
					
					# An integrity check:
					if first_part != suff:
						# This must be the case
						print "ABORTING: Error in tractus.insert failure"
						sys.exit()
					
					# Construct new intermediate node
					mid_node = Node()
					root.add_tag_below(tag_val) # Add new tag below root
					mid_node.add_tag_on(tag_val) # Add new tag on mid_node
					mid_node.tract_so_far = root.tract_so_far + first_part
					# All tags below root are now below mid_node
					mid_node.tags_below = root.get_tags_below() 
					# Construct an edge from root to mid_node
					root_mid_edge = Edge(root, mid_node, first_part)
					# Remove the old edge
					root.edges.pop(root.edges.index(edge)) 
					root.add_edge(root_mid_edge)
					# construct a node from mid_node to the end node
					mid_end_edge = Edge(mid_node, edge.end_node, last_part)
					mid_node.add_edge(mid_end_edge)
					return root
				else:
					# True Split: The shared prefix is only part of this edge
					# First split the edge.tract into its two parts
					first_part = edge.tract[0:pref]
					last_part = edge.tract[pref:]
					rest_of_suff = suff[pref:]
					# Construct a new intermediate node
					mid_node = Node()
					mid_node.tract_so_far = root.tract_so_far + first_part
					mid_node.tags_below = edge.end_node.get_tags_below() # get all tags below end node 
					mid_node.tags_below += edge.end_node.get_tags_on() # also include tags on the end node
					mid_node.add_tag_below(tag_val) # include the current tag
					# Construct an edge from root to mid_node
					root_mid_edge = Edge(root, mid_node, first_part)
					# Construct an edge from mid_node to end of this edge node
					mid_end_edge = Edge(mid_node, edge.end_node, last_part)
					mid_node.add_edge(mid_end_edge)
					# Remove the old edge
					root.edges.pop(root.edges.index(edge)) 
					root.add_edge(root_mid_edge)
					# Recursively add the rest of the suffix to mid_node
					mid_node = insert(mid_node, rest_of_suff, tag_val)
					return root

					
		if not common_pref_found:
			# No common prefix was found
			return add_suff_to_root()

# NOTE: always modify 'tag' and 'untag' together to
# maintain compatibility 
global tag
global untag
def tag(hap_val):
	# Create a unique string tag given a hap_val
	return "$" + str(hap_val) + "$"

def untag(tag_str):
	# Create get the integer of a tag string
	# Essentially avoid the first and last '$' characters
	return int(tag_str[1:-1])

### Parse Command Line ###
try:
	file_name = sys.argv[1]
	K = int(sys.argv[2])
	f = open(file_name, 'r')
except:
	print "ERROR: parsing command line arguments"
	print "Usage: >> tract_tree.py [input_file_name] [k]"
	print "k is the chosen number of expression classes"
	sys.exit()

### Parse the Input File ###
# Every line of the file should be of the format:
# haplotype \t expression value  

haps = [] # initialize haps, which will store all haplotypes
exp_vals = [] # initialize exp_vals, which will store paired expression values

# Now iterate through every line in the file 
for line in f:
	split_line = line.split('\t')
	this_hap = tractize([int(x) for x in list(split_line[0])]) # a list of ints
	haps.append(this_hap)
	exp_vals.append(float(split_line[1]))

# Close the Input File
f.close()

# Get the number and dimensions of the haplotype data
#(num_haps, hap_len) = np.shape(haps)
num_haps = len(haps)
hap_len = len(haps[0])



### Construct the Tractus Tree ### 
# The tree is constructed using a naive suffix tree construct algorithm, with
# runtime O(n^2) in the length of the input strings. The tradeoff is that we are
# able to directly incorporate a system of tagging for ease of access later on.
# For future revision, I would consider re-implementing using Ukkonen's linear time 
# suffix tree construction algorithm.

root = Node() # root of the tractus tree
for i in [0,1,3]:#range(num_haps):
	hap = haps[i] # get the i-th haplotype to be added to tree
	tag_val =  tag(i) # generate a unique tag for the i-th haplotype
	for j in range(hap_len):
		suffix = hap[j:] # get the j-th suffix of the haplotype
		root = insert(root, suffix, tag_val) # insert suffix into the Tractus tree
		
# Print the Tractus tree to stdout 
# print_tractus_tree(root)



### Collect Tag Sets from Tractus Tree ###
# Use depth-first traversal of tree to collect the sets of tags associated
# at each node. These tag sets will be used to train the two different models. 

# shared_tracts is a list of tuples, where each tuple is of the form:
# (<the tract in list form>, <length of tract>, <list of tags in integer form>)
# Each tuple refers to a tract in the Tractus tree that is shared by at least
# two haplotypes. Shared tracts are easily picked out by observing the tags
# at each node. 
shared_tracts = []

# tract_map is a list that maps a haplotype's index to a list
# tract indices. Each index in the list of tract indices refers
# to an element of the shared_tracts structure above.
# Ie. tract_map[i] = a list of indices into shared_tracts that 
# correspond to tracts that haplotype "i" shares with at least 
# one other haplotype
tract_map = [[] for x in range(num_haps)]

def collect_tags(root):
	# Traverse the tree given by root and populate
	# shared_tracts and tract_map accordingly
	# "untag" is a fn designed to convert root's tags to ints
	# Returns a tuple: (<shared_tracts>, <tract_map>)
	shared_tracts = []
	tract_map = [[] for x in range(num_haps)]

	def search_node(node):
		# Searches a single node and updates shared_tracts
		# and tract_map accordingly
		all_tags = node.get_tags_below() + node.get_tags_on()
		if len(all_tags) > 1:
			untagged_list = map(untag, all_tags)
			shared_tracts.append((node.tract_so_far, len(node.tract_so_far), untagged_list))
			tract_ind = len(shared_tracts) # since this is the most recently added tract
			# Populate tract_map accordingly
			for hap in untagged_list:
				tract_map[hap].append(tract_ind)
			# Recursively search nodes at the end of each outgoing edge
			for edge in node.edges:
				search_node(edge.end_node)

	# Skip the root node (since it does not refer to a tract)
	# Begin by searching all of its edges
	for edge in root.edges:
		# Search each child node
		search_node(edge.end_node)

	# Output the populated data structures
	return (shared_tracts, tract_map)

# Run collect_tags on the root of the Tractus tree
# Ie., perform depth-first traversal of the Tractus tree to 
# populate shared_tracts and tag_map 
(shared_tracts, tract_map) = collect_tags(root)
for tract in shared_tracts:
	print tract[0]

# Function to calculate the average shared tract length
def avg_tract_length(shared_tracts):
	num_shared_tracts = len(shared_tracts)
	tract_lens = [x[1] for x in shared_tracts]
	return float(sum(tract_lens)) / float(num_shared_tracts)

# Label each haplotype with one of K expression levels
# based on paired expression data
def generate_exp_lvl_vec(exp_vec, K):
	# Outputs a list of size exp_vec where each value
	# has been converted to a value in [1,..., K]
	lvl_size = float(max(exp_vec) - min(exp_vec)) / float(K)
	min_val = float(min(exp_vec))
	# Initialize vector of level assignment
	lvl_vec = [0 for x in range(len(exp_vec))]
	# Assign each value in exp_vec to a level and store it in lvl_vec
	for i in range(len(exp_vec)):
		exp_val = exp_vec[i]
		for k in range(K):
			if exp_val <= (min_val + (k+1)*lvl_size):
				lvl_vec[i] = k #assign level vec
				break # exit loop
	return lvl_vec

# Generate the expression level vector
# E[i] = the expression level of haplotype i
# Values in E are integers [0,...,K-1]
E = generate_exp_lvl_vec(exp_vals, K)


### N-fold Cross Validation Using the Voting Theory Method ###
# Take out every haplotpye individually and classify it / predict
# its expression based on the voting theory approach.

# def calculate_confidence(tract, hap_ind, E):
# 	# Calculates the vote and confidence of this tract
# 	# for the haplotype specified by hap_ind
# 	# E[i] is the expression level of haplotype i
# 	tract_tags = tract[2] # the tags associated with this tract
# 	tract_tags.remove(hap_ind) # remove the hap we are trying to predict



# predictions = [0 for x in range(num_haps)]
# for i in range(num_haps):
# 	# Form a prediction of the expression level of haplotype "i"
# 	hap = haps[i]
# 	score_vector = [0 for k in range(K)] # will store scores for each class
# 	tract_inds = tract_map[i]
# 	for ind in tract_inds:
# 		tract = shared_tracts[ind]
# 		L = tract[1] # length of the tract















