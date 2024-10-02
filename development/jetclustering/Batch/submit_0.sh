universe=vanilla
executable=job_0.sh
+JobFlavour="espresso"
RequestCpus=1
should_transfer_files=YES
when_to_transfer_output=ON_EXIT_OR_EVICT
transfer_input_files=/afs/cern.ch/user/p/pryadav/public/COFFEA-FCC/coffea-fcc-analyses/development/jetclustering/Batch/job_0.py,/afs/cern.ch/user/p/pryadav/public/COFFEA-FCC/coffea-fcc-analyses/development/jetclustering/processor.py
transfer_output_files=singularity.log.job_0,jetclustering.coffea
output=out-0.$(ClusterId).$(ProcId)
error=err-0.$(ClusterId).$(ProcId)
log=log-0.$(ClusterId).$(ProcId)
queue 1