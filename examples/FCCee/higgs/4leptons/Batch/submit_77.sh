universe=vanilla
executable=job_77.sh
+JobFlavour="longlunch"
RequestCpus=1
should_transfer_files=YES
when_to_transfer_output=ON_EXIT_OR_EVICT
transfer_input_files=/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/Batch/job_77.py,/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/processor.py,/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/config.py,/afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/Batch/scripts.tar, /afs/cern.ch/user/p/pryadav/coffea-fcc-analyses/examples/FCCee/higgs/4leptons/functions.py,
transfer_output_files=singularity.log.job_77,4leptons-chunk77.coffea
output=out-77.$(ClusterId).$(ProcId)
error=err-77.$(ClusterId).$(ProcId)
log=log-77.$(ClusterId).$(ProcId)
queue 1