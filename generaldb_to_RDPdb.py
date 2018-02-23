################################################################################
#	Written by Natalie Vande Pol											   #
#	Jun 13, 2016															   #
#																			   #
#	*   command line: python generaldb_to_RDP.py [path/filename(s)]	   		   #
#	*   accepts unlimited reference database files and converts them to fasta  #
#		and taxonomy files in the RDP format								   #
#	*   output files written to original file locations, the initial filenames #
#		appended "__RDP.fasta" and "__RDP_taxonomy.txt"						   #
################################################################################

import sys, os

num = 0
for arg in sys.argv[1:]:
	gen = open(arg, "r")
	all_lines = gen.readlines()
	gen.close()

	fasta = open(".".join(os.path.splitext(arg)[:-1])+"__RDP.fasta","w")
	taxon = open(".".join(os.path.splitext(arg)[:-1])+"__RDP_taxonomy.txt","w")
	taxon.write("Seq_ID\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")	

	for i, line in enumerate(all_lines):
		if line[0]==">":
			temp = line[1:].split("|")
			name = str(temp[1])
			temp2 = temp[4].strip().split("__")
			to_genus = [ item[:-2] for item in temp2[1:-1] ]
			
			if "Incertae_sedis" in to_genus:
				indices = [i for i,x in enumerate(to_genus) if x == "Incertae_sedis"]
				for j in indices:
					if "Incertae_sedis" not in to_genus[j-1]:
						to_genus[j] = str(to_genus[j-1])+"_Incertae_sedis"
					else:
						to_genus[j] = str(to_genus[j-1])
			if "unidentified" in to_genus:
				indices = [i for i,x in enumerate(to_genus) if x == "unidentified"]
				for j in indices:
					if "unidentified" not in to_genus[j-1]:
						to_genus[j] = str(to_genus[j-1])+"_unidentified"
					else:
						to_genus[j] = str(to_genus[j-1])
			
			species = str(temp2[-1]).replace("_"," ")
			if species.endswith("sp"):
				species+= str(num)
				num += 1
			
			fasta.write(">"+name+"\n")
			taxon.write(name+"\t"+"\t".join(to_genus)+"\t"+species+"\n")
		
		else:
			fasta.write(line)
	fasta.close()
	taxon.close()


