import os
import argparse
#import re

parser = argparse.ArgumentParser()
#parser.add_argument("-rdir", "--root-directory", type=str, nargs='?', help="Path to directory containing root files")
parser.add_argument("-f", "--filename", type=str, nargs='?', help="Path to input files for condor")
parser.add_argument("-b", "--batch-size", type=int, nargs='?')
parser.add_argument("-N", "--dataset-size", type=int, nargs='?')
parser.add_argument("-s", "--stem", type=str, nargs='?')
args = parser.parse_args()

resubmit_jobs = []

for i in range(args.dataset_size):
    name = args.stem + '{}.root'.format(i)
    if not os.path(name):
        resubmit_jobs.append(i)
    else:
        info = os.popen("ls -l {}".format(name)).split()
        if int(info[4]) < 50000:
            resubmit_jobs.append(i)

'''
files = os.popen("ls -l {}".format(args.root_directory)).readlines()[1:]
for f in files:
    f = f.split() # ['-rw-r--r--.', '1', 'adlintul', 'zh', '175', '8.', 'Apr', '14:29', 'JRA_0.root\n']
    name = f[-1]
    if name.find(".root") != -1:
        if int(f[4]) < 50000:
            number = re.findall(r'\d+', name)
            if number:
                resubmit_jobs.append(number[-1]) # assumes last number in name is job_id
'''

old = None
new = None
try:
    old = open(args.filename, 'r')
    lines = old.readlines()
    new = open(args.filename.replace('.txt', '_resubmit') + '.txt', 'w+')
    for job in resubmit_jobs:
        start = job * args.batch_size
        for i in range(args.batch_size):
            new.write(lines[start + i])
finally:
    if old is not None:
        old.close()
    if new is not None:
        new.close()
        print 'Printed jobs to resubmit at ' + args.filename.replace('.txt', '_resubmit') + '.txt'
