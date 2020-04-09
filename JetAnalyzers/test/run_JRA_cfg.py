from JetMETAnalysis.JetAnalyzers.addAlgorithm import addAlgorithm
import JetMETAnalysis.JetAnalyzers.Defaults_cff as Defaults
import FWCore.ParameterSet.Config as cms
import sys
import os
import argparse
from itertools import islice

inputfile = 'root://cmsxrootd.fnal.gov///store/mc/RunIIAutumn18DRPremix/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/AODSIM/102X_upgrade2018_realistic_v15_ext1-v1/60000/3D5DC49F-5E3B-CD4A-9354-C722F143D3B1.root'
outputfile = 'JRA.root'
progName = sys.argv[1]

parser = argparse.ArgumentParser(description='Change the option prefix characters',
                                 prefix_chars='+/',
                                 )
parser.add_argument("cfgfilename", default=progName, action='store', help=argparse.SUPPRESS)
parser.add_argument("+i", "++input", nargs='+', type=str)
#parser.add_argument("+i", "++input", type=str, nargs='?', default=inputfile, const=inputfile, help="Text file with names of root files")
parser.add_argument("+o", "++output", type=str, nargs='?', default=outputfile, const=outputfile, help="Name of output file")
#parser.add_argument("+sf", "++start-files", type=int, nargs='?', default=0, const=0, help="Start files from here")
#parser.add_argument("+nf", "++number-files", type=int, nargs='?', default=1, const=1, help="Number of root files to read from input")
parser.add_argument("+ne", "++number-events", type=int, nargs='?', default=1000, const=1000, help="Number of events")
args = parser.parse_args()

#!
#! PROCESS
#!
# Conditions source options: GT, SQLite, DB
conditionsSource = "GT"
era = "Spring16_25nsV1_MC"
doProducer = False
process = cms.Process("JRA")
multithread = False
if doProducer:
    process = cms.Process("JRAP")
    multithread = True


#!
#! CHOOSE ALGORITHMS
#!
# Note: Not all combinations of options will work
# Algorithm options: ak, kt, ic, sc, ca
# Size options: integers 1-10
# Jet type options: calo, pf, pfchs, puppi
# Correction levels: '' (blank), l1, l2, l3, l2l3, l1l2l3
algsizetype = {'ak': [4, 8]}
jettype = ['pf', 'pfchs', 'puppi']
corrs = ['']

algorithms = []
jcr = cms.VPSet()

for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            for c in corrs:
                algorithms.append(str(k+str(s)+j+c))
                if conditionsSource != "GT":
                    upperAlg = str(
                        k.upper()+str(s)+j.upper().replace("CHS", "chs")).replace("PUPPI", "PFPuppi")
                    jcr.append(cms.PSet(record=cms.string("JetCorrectionsRecord"),
                                        tag=cms.string(
                                            "JetCorrectorParametersCollection_"+era+"_"+upperAlg),
                                        label=cms.untracked.string(upperAlg)))

# If need be you can append additional jet collections using the style below
# algorithms.append('ak5calo')


#!
#! CONDITIONS (DELIVERING JEC BY DEFAULT!)
#!
process.load(
    "Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = cms.string('102X_upgrade2018_realistic_v15')

if conditionsSource != "GT":
    if conditionsSource == "DB":
        conditionsConnect = cms.string(
            "frontier://FrontierPrep/CMS_COND_PHYSICSTOOLS")
    elif conditionsSource == "SQLite":
        conditionsConnect = cms.string('sqlite_file:'+era+'.db')

    from CondCore.DBCommon.CondDBSetup_cfi import *
    process.jec = cms.ESSource("PoolDBESSource", CondDBSetup,
                               connect=conditionsConnect,
                               toGet=cms.VPSet(jcr))
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource", "jec")


#!
#! INPUT
#!
nevents = args.number_events
print 'nevents (default=1000)  = {}'.format(nevents)
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(nevents))

##############################################
# External Input File (most likely from DAS) #
##############################################

#filename = os.environ.get('INPUTFILES', 'filenames.txt')
'''
filename = args.input
nfiles = args.number_files
print 'nfiles (default=1)  = {}'.format(nfiles)

inputfiles = []
f = None
try:
    f = open(filename, 'r')
    if nfiles > 0:
        inputfiles = ['root://cmsxrootd.fnal.gov//'+line[1:-2] for line in islice(f, args.start_files, args.start_files + nfiles)]
    else:
        inputfiles = ['root://cmsxrootd.fnal.gov//'+line[1:-2] for line in f]
finally:
    if f is not None:
        f.close()
'''

inputfiles = args.input

print inputfiles

process.source = cms.Source(
    "PoolSource", fileNames=cms.untracked.vstring(*inputfiles))

outputname = args.output

#!
#! SERVICES
#!
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))
if doProducer:
    process.add_(cms.Service("Tracer"))
    process.options.numberOfThreads = cms.untracked.uint32(8)
    process.options.numberOfStreams = cms.untracked.uint32(0)
else:
    process.load('CommonTools.UtilAlgos.TFileService_cfi')
    process.TFileService.fileName = cms.string(outputname)


#!
#! NEEDED FOR PFCHS
#!
process.load('CommonTools.ParticleFlow.pfNoPileUpJME_cff')
process.pfPileUpJME.checkClosestZVertex = False


#!
#! JET & REFERENCE KINEMATIC CUTS
#!


#!
#! RUN JET RESPONSE ANALYZER
#!

# set to False to use jets from the input file (NOT RECOMMENDED)
doJetReco = True
outCom = cms.untracked.vstring('drop *')
for algorithm in algorithms:
    if (algorithm.find('HLT') > 0):
        process.load("Configuration.Geometry.GeometryIdeal_cff")
        process.load("Configuration.StandardSequences.MagneticField_cff")
        addAlgorithm(process, algorithm, Defaults, False, doProducer)
    else:
        addAlgorithm(process, algorithm, Defaults, doJetReco, doProducer)
    outCom.extend(['keep *_'+algorithm+'_*_*'])


#!
#! Check the keep and drop commands being added to the outputCommamnds
#!
printOC = False
if printOC:
    for oc in outCom:
        print oc


#!
#! Output
#!

if doProducer:
    process.out = cms.OutputModule("PoolOutputModule",
                                   fileName=cms.untracked.string(outputname),
                                   outputCommands=outCom
                                   )
    process.e = cms.EndPath(process.out)


#!
#! THAT'S ALL! CAN YOU BELIEVE IT? :-D
#!

# Not sure what this does
#processDumpFile = open('runJRA.dump' , 'w')
#print >> processDumpFile, process.dumpPython()
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))
process.options.allowUnscheduled = cms.untracked.bool(True)
