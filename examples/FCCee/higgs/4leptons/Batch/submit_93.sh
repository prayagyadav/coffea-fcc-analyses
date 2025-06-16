universe=vanilla
executable=job_93.sh
+JobFlavour="longlunch"
RequestCpus=1
should_transfer_files=YES
when_to_transfer_output=ON_EXIT_OR_EVICT
transfer_input_files=/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/Batch/job_93.py,/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/processor.py,/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/config.py,/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/Batch/scripts.tar, /afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/functions.py,
transfer_output_files=singularity.log.job_93,4leptons-chunk93.coffea
output=out-93.$(ClusterId).$(ProcId)
error=err-93.$(ClusterId).$(ProcId)
log=log-93.$(ClusterId).$(ProcId)
queue 1