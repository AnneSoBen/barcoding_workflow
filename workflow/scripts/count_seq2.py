import re
import pandas as pd
import subprocess


def count_all_seq(obifasta):
	n = 0
	file = open(obifasta, "r")
	for line in file:
		if re.search("^>", line):
			a = line.split("; ")
			for value in a:
				if 'count' in value:
					b = value.split("=")
					n += int(b[1])
	return(n)


derepl_uniq = len([1 for line in open(snakemake.input.derepl) if re.match('^>', line)])
derepl_seq = count_all_seq(snakemake.input.derepl)
basicfilt_uniq = len([1 for line in open(snakemake.input.filt) if re.match('^>', line)])
basicfilt_seq = count_all_seq(snakemake.input.filt)
basicfilt_uniq_p = round(float(basicfilt_uniq)/float(derepl_uniq)*100,1)
basicfilt_seq_p = round(float(basicfilt_seq)/float(derepl_seq)*100,1)

clust_uniq = len([1 for line in open(snakemake.input.clust) if re.match('^>', line)])
clust_seq = count_all_seq(snakemake.input.clust)

df = pd.DataFrame(columns = ['lib', 'file', 'uniq_seq', 'perc_kept_uniq', 'seq', 'perc_kept_seq', 'motus'],
	index = ['dereplicated', 'basicfilt', 'clustering'])

df['lib'] = [snakemake.params.lib_name]*3
df['file'] = ['dereplicated', 'basicfilt', 'clustering']
df['uniq_seq'] = [derepl_uniq, basicfilt_uniq, '-']
df['perc_kept_uniq'] = ['-', basicfilt_uniq_p, '-']
df['seq'] = [derepl_seq, basicfilt_seq, clust_seq]
df['perc_kept_seq'] = ['-', basicfilt_seq_p, '-']
df['motus'] = ['-', '-', clust_uniq]

df.to_csv(snakemake.output.tab2, sep='\t', index=False)

