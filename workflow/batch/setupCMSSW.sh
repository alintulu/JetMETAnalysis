#!/bin/bash

[[ -z "$1" ]] && { echo "Provide path to proxy certificate" ; exit 1; }

export X509_USER_PROXY=$1
cd /afs/cern.ch/user/a/adlintul/CMSSW_10_6_1/src
eval `scramv1 runtime -sh`
