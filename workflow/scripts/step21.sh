#!/bin/bash

source scripts/env.sh

# fit Gaussian to histogram
jet_response_fitter_x -input $inDIR/JRA_l1.root \
		-output $inDIR/JRA_l1_f.root \
		-niter 100
