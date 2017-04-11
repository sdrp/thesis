# Get haps from real data

import sys

# Hardcoded list of SRR numbers
srr_list = ["SRR1304947", "SRR1304967", "SRR1304987", "SRR1305009", "SRR1305127", "SRR1305287", "SRR1305319", "SRR1305565", "SRR1305587", "SRR1305673", "SRR1305809", "SRR1305831", "SRR1305939", "SRR1305991", "SRR1306141"]

# The gtex ids of the corresponding elements of srr_list
gtex_ids = ["GTEX-Q2AI-0003-SM-3UZFI", "GTEX-X8HC-0003-SM-3UZEU", "GTEX-WFON-0003-SM-3UZES", "GTEX-W5WG-0003-SM-3UZF6", "GTEX-QEG5-0003-SM-3USS5", "GTEX-S7SF-0003-SM-3USSM", "GTEX-R55C-0003-SM-3USSH", "GTEX-P4PQ-0003-SM-3UZFF", "GTEX-QDVN-0003-SM-3UZFJ", "GTEX-R53T-0003-SM-3UZFQ", "GTEX-WFJO-0003-SM-3UZER", "GTEX-S3XE-0003-SM-3UZFM", "GTEX-RVPV-0003-SM-3USSI", "GTEX-R55E-0003-SM-3UZFL", "GTEX-PLZ5-0003-SM-3UZFG"]

# Open the output file
out = open('real_haps_KCNJ12', 'w')

for srr_num in srr_list:
	print srr_num
	f = open(srr_num+"_hap_result", 'r')
	found = False
	while not found:
		# Search until the beginning of the long block is found
		line = f.readline()
		if line.startswith("487745"):
			found = True
			hap_str = ""
			for i in range(42):
				hap_line = f.readline()
				split_hap_line = hap_line.split("\t")
				if split_hap_line[2] == '2':
					hap_str = hap_str + '1' # 2 represents an error, correct it arbitrarily
				else:
					hap_str = hap_str + split_hap_line[2]
			out.write(hap_str + "\n")
	f.close()

# Close the output file
out.close()