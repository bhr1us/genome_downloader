##This script downloads the latest summary assembly table from NCBI.
##Script downloads fasta files
#Run this script in its own directory 
#Usage: genome_downloader.py ["organism name"] [genome type]
#genome type can be "complete" or "all" genomes

import sys
import os
import re
import urllib.request
import argparse
from Bio import SeqIO
from Bio import Entrez

#help documentation
parser = argparse.ArgumentParser(
	description = '''Description: Run this script in separate folder.  Downloads latest NCBI assembly summary file and genomes in FASTA format.''')
parser.add_argument('organism_name', help = 'matches genus or full species name')
parser.add_argument('genome_type', help = 'indicate complete or all genomes')
args=parser.parse_args()

## NCBI needs your email
email_Address = "bhr1us@gmail.com"
Entrez.email = email_Address

#Download assembly_summary table form NCBI
##Uncomment to allow genome table download
print ("Downloading NCBI genome assembly seqeunces table...\n")
urllib.request.urlretrieve("ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt", "assembly_summary.txt")

#Parse sys.argv
species = sys.argv[1]
asbly_level = sys.argv[2]

#empty list to hold ftp addresses
list = []

#define functions for selecting ftp addresses
def AllGenomes():
	statsfile = open("assembly_summary.txt", "r", encoding='UTF8')
	for line in statsfile.readlines():
		if line.startswith("#"):
			pass
		else:
			line = line.split("\t")
		if re.search(species, line[7]):
			list.append(line[19])

def CompleteGenomes():
	statsfile = open("assembly_summary.txt", "r", encoding='UTF8')
	for line in statsfile.readlines():
		if line.startswith("#"):
			pass
		else:
			line = line.split("\t")
		if re.search(species, line[7]) and (line[11] == "Complete Genome"):
			list.append(line[19])

#read lines in assembly statistics table
if asbly_level == "all":
	AllGenomes()
	print ("There are " + str(len(list)) + " " + species +" COMPLETE & DRAFT genomes.\n")
	print ("Downloading genome files...\n")
elif asbly_level == "complete":
	CompleteGenomes()
	print ("There are " + str(len(list)) + " " + species +" COMPLETE genomes.\n")
	print ("Downloading genome files...\n")
else:
	print ("Please choose 'complete' or 'all' Genomes!")

#download genomes in fasta format
for i in list:
	gen_name = i.split("/")
	gen_name = gen_name[9]
	url = i + "/" + gen_name + "_genomic.fna.gz"
	filenamesave = gen_name + "_genomic.fna.gz"
	urllib.request.urlretrieve(url, filenamesave)

print ("Genome download completed!")
