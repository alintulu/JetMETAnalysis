import os
import argparse
from itertools import islice

parser = argparse.ArgumentParser(description='Change the option prefix characters',
                                 prefix_chars='+/',
                                 )
parser.add_argument("+b", "++batch-size", type=int, nargs='?', default=1, const=1)
parser.add_argument("+nf", "++number-files", type=int, nargs='?', default=1, const=1)
parser.add_argument("+i", "++input", type=str, nargs='?')
args = parser.parse_args()
nfiles = args.number_files
batch_size = args.batch_size

bash_cmd = 'cmsRun JetMETAnalysis/JetAnalyzers/test/run_JRA_cfg.py +o JRA_PU_{}.root +i'

print 'Starting jobs...'

f = None
bash_cmd_job = ""
idx = batch_size - 1
try:
    f = open(args.input, 'r')
    for i, line in enumerate(f):
        if nfiles > 0 and i >= nfiles:
            break
        if i % batch_size == 0:
            if i == 0:
                bash_cmd_job = bash_cmd.format(0)
            else:
                bash_cmd_job = bash_cmd.format(i - idx)
                idx += batch_size - 1
        bash_cmd_job += " root://cmsxrootd.fnal.gov//{}".format(line[1:-2])
        if (i + 1) % batch_size == 0:
            print 'Start job {}'.format(i - batch_size + 1)
            os.system(bash_cmd_job)
finally:
    if f is not None:
        f.close()

