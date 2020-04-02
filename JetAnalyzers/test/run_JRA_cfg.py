import FWCore.ParameterSet.Config as cms

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
algsizetype = {'ak':[4,8]}
jettype = ['pf','pfchs','puppi']
corrs = ['']

algorithms = []
jcr = cms.VPSet()

for k, v in algsizetype.iteritems():
    for s in v:
	for j in jettype:
            for c in corrs:
	        algorithms.append(str(k+str(s)+j+c))
	        if conditionsSource != "GT":
                    upperAlg = str(k.upper()+str(s)+j.upper().replace("CHS","chs")).replace("PUPPI","PFPuppi")
		    jcr.append(cms.PSet(record = cms.string("JetCorrectionsRecord"),
					tag = cms.string("JetCorrectorParametersCollection_"+era+"_"+upperAlg),
					label= cms.untracked.string(upperAlg)))

# If need be you can append additional jet collections using the style below
#algorithms.append('ak5calo')


#!
#! CONDITIONS (DELIVERING JEC BY DEFAULT!)
#!
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = cms.string('102X_upgrade2018_realistic_v15')

if conditionsSource != "GT":
    if conditionsSource == "DB":
        conditionsConnect = cms.string("frontier://FrontierPrep/CMS_COND_PHYSICSTOOLS")
    elif conditionsSource == "SQLite":
	conditionsConnect = cms.string('sqlite_file:'+era+'.db')    

    from CondCore.DBCommon.CondDBSetup_cfi import *
    process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
			       connect = conditionsConnect,
			       toGet =  cms.VPSet(jcr))
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource","jec")


#!
#! INPUT
#!
nevents = int(os.environ.get('NEVENTS','1000'))
print('nevents (default=1000)  = %d'.format(nevents))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(nevents))

##############################################
# External Input File (most likely from DAS) #
##############################################

inputfiles = []
filename = os.environ.get('INPUTFILES','filenames.txt')
try:
    f = open(filename)
    for line in f:
        inputfiles.append('root://cmsxrootd.fnal.gov//'+line[1:-2]) # first char " last two chars "\n
finally:
    f.close()
else:
    inputfiles = 'root://cmsxrootd.fnal.gov///store/mc/RunIIAutumn18DRPremix/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/AODSIM/102X_upgrade2018_realistic_v15_ext1-v1/60000/3D5DC49F-5E3B-CD4A-9354-C722F143D3B1.root'

inputfiles = inputfiles[:5] # truncate while testing
print(inputfiles)

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(*inputfiles))

#!
#! SERVICES
#!
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))
if doProducer:
    process.add_(cms.Service("Tracer"))
    process.options.numberOfThreads = cms.untracked.uint32(8)
    process.options.numberOfStreams = cms.untracked.uint32(0)
else:
    process.load('CommonTools.UtilAlgos.TFileService_cfi')
    process.TFileService.fileName=cms.string('JRA.root')


#!
#! NEEDED FOR PFCHS
#!
process.load('CommonTools.ParticleFlow.pfNoPileUpJME_cff')
process.pfPileUpJME.checkClosestZVertex = False


#!
#! JET & REFERENCE KINEMATIC CUTS
#!
import JetMETAnalysis.JetAnalyzers.Defaults_cff as Defaults


#!
#! RUN JET RESPONSE ANALYZER
#!

# set to False to use jets from the input file (NOT RECOMMENDED)
doJetReco = True
outCom = cms.untracked.vstring('drop *')
from JetMETAnalysis.JetAnalyzers.addAlgorithm import addAlgorithm
for algorithm in algorithms:
    if (algorithm.find('HLT') > 0) :
        process.load("Configuration.Geometry.GeometryIdeal_cff")
        process.load("Configuration.StandardSequences.MagneticField_cff")
        addAlgorithm(process,algorithm,Defaults,False,doProducer)
    else:
        addAlgorithm(process,algorithm,Defaults,doJetReco,doProducer)
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
				   fileName = cms.untracked.string('JRAP.root'),
				   outputCommands = outCom
				   )
    process.e = cms.EndPath(process.out)


#!
#! THAT'S ALL! CAN YOU BELIEVE IT? :-D
#!

#Not sure what this does
#processDumpFile = open('runJRA.dump' , 'w')
#print >> processDumpFile, process.dumpPython()
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)
