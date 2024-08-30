import re
import pandas as pd
import subprocess

R1 = len([1 for line in open(snakemake.input.R1) if re.match('^\+$', line)])
R2 = len([1 for line in open(snakemake.input.R2) if re.match('^\+$', line)])
paired = len([1 for line in open(snakemake.input.R1R2) if re.match('^\+$', line)])
good_ali = len([1 for line in open(snakemake.input.good) if re.match('^\+$', line)])
good_ali_p = round(float(good_ali)/float(paired)*100,1)
bad_ali = len([1 for line in open(snakemake.input.bad) if re.match('^\+$', line)])
bad_ali_p = round(float(bad_ali)/float(paired)*100,1)
demult = len([1 for line in open(snakemake.input.demult) if re.match('^>', line)])
demult_p = round(float(demult)/float(good_ali)*100,1)
unassigned = len([1 for line in open(snakemake.input.unass) if re.match('^>', line)])
unassigned_p = round(float(unassigned)/float(good_ali)*100,1)

df = pd.DataFrame(columns = ['lib', 'file', 'reads', 'perc_kept_lost'],
	index = ['R1', 'R2', 'paired', 'good_ali', 'bad_ali', 'demultiplexed', 'unassigned'])

df['lib'] = [snakemake.params.lib_name]*7
df['file'] = ['R1', 'R2', 'paired', 'good_ali', 'bad_ali', 'demultiplexed', 'unassigned']
df['reads'] = [R1, R2, paired, good_ali, bad_ali, demult, unassigned]
df['perc_kept_lost'] = ['-', '-', '-', good_ali_p, bad_ali_p, demult_p, unassigned_p]

df.to_csv(snakemake.output.tab1, sep='\t', index=False)
