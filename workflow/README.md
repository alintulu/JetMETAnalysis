# Workflow

* [batch](workflow/batch)
  Contains files for submitting a batch job
* [scripts](workflow/scripts)
  Contains various helper scripts such as _merging ntuples_ and _resubmitting jobs_
 
## Step10: Create ntuples
 
### Submit batch job
  
First step of the JEC workflow is creating ntuples out of the dataset files. It's quite
cumbersome and done as a batch job.
The executable is [step10_ntuple.sh](workflow/batch/step10_ntuple.sh) and
arguments passed to it is:

1. Valid proxy certificate
2. Cluster id _(currently unecessary)_
3. Job id
4. Path to file containing names of files to run over,
 `dasgoclient -query="file dataset=$DATASET" -json | jq . | jq ".[].file[].name" > filenames.txt`
5. Batch size, i.e. how many files per job
6. Number of events, 0 for all events
7. Name of output folder, PU or noPU

### Resubmit jobs

When batch job is done you need to loop over output files to
check if some jobs failed and resubmitting them is necessary. It's done with [resubmit.py](workflow/scripts/resubmit.py) that takes

* `-f`  Path to file containing names of files that was given to batch job
* `-b`  Batch size, same as for batch job submission
* `-N`  Number of output files (number of batch jobs)
* `-s`  Stem of name of output files, e.g. `JRA` for `JRA0.root`

The script loops over all output files that should have been created and
1. Checks if file exist
2. Check if size of file is larger than 50000

If any of above fails then the id of the job will be noted and names of files beloning to that job will be added
for resubmission.

### Merge ntuples

Batch job created mutiple root files (probably around 200-300). Merging them into one file is done
with the command `hadd` and is done recursively with [merge.sh](workflow/scripts/merge.sh). The script takes

* Stem of output files, e.g. `JRA` for `JRA0.root`
* Batch size, in this case how many files to merge at once

## Rest of the steps...

Bash scripts for running the rest for the steps, is located in [scripts](workflow/scripts).
Files namned `step1{1..3}.sh` computes and applies L1 corrections. 
Files namned `step2{0..3}.sh` computes and applies L2L3 corrections.
Scripts need some adjusting, but hey at least they run!

The script [step11.sh](workflow/scripts/step11.sh) creates the PU distributions for data and MC.

## To Do

- Some path are weird after creating `workflow` directory'
and adding folder `batch` and `scripts` inside of `JetMET`


