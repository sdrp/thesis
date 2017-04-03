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
					# We take the additional part of the suffix and add a new edge
					root.add_tag_below(tag_val)
					rest_of_suff = suffix[pref:]
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
					root.add_edge(root_mid_edge)
					# construct a node from mid_node to the end node
					mid_end_edge = Edge(mid_node, edge.end_node, last_part)
					mid_node.add_edge(mid_end_edge)
					# Remove the old edge
					root.edges.pop(root.edges.index(edge)) 
					return root
				else:
					# True Split: The shared prefix is only part of this edge
					# First split the edge.tract into its two parts
					first_part = edge.tract[0:pref]
					last_part = edge.tract[pref:]
					rest_of_suff = suffix[pref:]
					# Construct a new intermediate node
					mid_node = Node()
					mid_node.tract_so_far = root.tract_so_far + first_part
					mid_node.tags_below = edge.end_node.get_tags_below() # get all tags below end node 
					mid_node.tags_below += edge.end_node.get_tags_on() # also include tags on the end node
					mid_node.add_tag_below(tag_val) # include the current tag
					# Construct an edge from root to mid_node
					root_mid_edge = Edge(root, mid_node, first_part)
					root.add_edge(root_mid_edge)
					# Construct an edge from mid_node to end of this edge node
					mid_end_edge = Edge(mid_node, edge.end_node, last_part)
					mid_node.add_edge(mid_end_edge)
					# Remove the old edge
					root.edges.pop(root.edges.index(edge)) 
					# Recursively add the rest of the suffix to mid_node
					mid_node = insert(mid_node, rest_of_suff, tag_val)
					return root

					
		if not common_pref_found:
			# No common prefix was found
			return add_suff_to_root()


def tag(hap_val):
	# Create a unique tag given a hap_val
	return "$" + str(hap_val) + "$"

### Parse Command Line ###
try:
	file_name = sys.argv[1]
	f = open(file_name, 'r')
except:
	print "ERROR: could not open file"

### Parse the Input File ###
# Every line of the file should be of the format:
# haplotype \t expression value  

# first_line = f.readline()
# split_line = first_line.split('\t')
# this_hap = np.asarray(tractize([int(x) for x in list(split_line[0])]))
haps = [] # initialize haps, which will store all haplotypes
exp_vals = [] # initialize exp_vals, which will store paired expression values

# Now iterate through every line in the file 
for line in f:
	split_line = line.split('\t')
	this_hap = tractize([int(x) for x in list(split_line[0])]) # a list of ints
	# haps = np.vstack( (haps, np.asarray(this_hap)) )
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
for i in [0,1,2]:#range(num_haps):
	hap = haps[i] # get the i-th haplotype to be added to tree
	tag_val =  tag(i) # generate a unique tag for the i-th haplotype
	for j in range(hap_len):
		suffix = hap[j:] # get the j-th suffix of the haplotype
		root = insert(root, suffix, tag_val) # insert suffix into the Tractus tree
		
# Print the Tractus tree to stdout 
print_tractus_tree(root)















