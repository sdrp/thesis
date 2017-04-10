# A python script to convert input SRA to BAM and then run hapcut on it

import sys
import os
import subprocess

# input_sra_number = sys.argv[1]

# Load samtools
subprocess.call("module load samtools/1.3.1", shell=True)

# Hardcoded list of SRR numbers
srr_list = [SRR1304947, SRR1304967, SRR1304987, SRR1305009, SRR1305127, SRR1305287, SRR1305319, SRR1305565, SRR1305587, SRR1305673, SRR1305809, SRR1305831, SRR1305939, SRR1305991, SRR1306141]
srr_names = [str(val) for val in srr_list]
for input_sra_number in srr_names
	# cp the sra file into the local ncbi folder
	cp_str = "cp /users/sperera/scratch/decrypted_data/sras/" + input_sra_number + ".sra /users/sperera/ncbi/dbGaP-13660/sra/"
	subprocess.call(cp_str, shell=True)

	# Convert the SRA to SAM
	sra2sam_string = "/users/sperera/thesis_code/SRA_Toolkit/sratoolkit/bin/sam-dump /users/sperera/ncbi/dbGaP-13660/sra/" + input_sra_number + ".sra > /users/sperera/scratch/decrypted_data/sams/" + input_sra_number + ".sam"
	subprocess.call(sra2sam_string, shell=True)
	print "1) Converted SRA to SAM!"

	# Convert the SAM to BAM
	sam2bam_string = "samtools view -Sb /users/sperera/scratch/decrypted_data/sams/" + input_sra_number + ".sam > /users/sperera/scratch/decrypted_data/bams/" + input_sra_number + ".bam"
	subprocess.call(sam2bam_string, shell=True)
	print "2) Converted SAM to BAM!"

	# Run extract hairs on BAM
	extract_hairs_string = "/users/sperera/thesis_code/hapcut-master/extractHAIRS --VCF /users/sperera/data/sperera/decrypted_data/vcfs/big_vcf.vcf --bam /users/sperera/data/sperera/decrypted_data/bams/" + input_sra_number + ".bam --maxIS 600 > /users/sperera/scratch/" + input_sra_number + "_fragmat"
	subprocess.call(extract_hairs_string, shell=True)

	# Run the hapcut algorithm
	hapcut_string = "/users/sperera/thesis_code/hapcut-master/HAPCUT --fragments /users/sperera/scratch/" + input_sra_number + "_fragmat  --VCF /users/sperera/data/sperera/decrypted_data/vcfs/big_vcf.vcf --output /users/sperera/scratch/" + input_sra_number + "_hap_result > /users/sperera/scratch/hapcut.log"
	subprocess.call(hapcut_string, shell=True)

	# Remove the file from ncbi directory
	rm_str = "rm /users/sperera/ncbi/dbGaP-13660/sra/" + input_sra_number + ".sra"
	subprocess.call(rm_str, shell=True)

	print "DONE WITH " + input_sra_number 


