universe=vanilla
executable=job_0.sh
+JobFlavour="espresso"
RequestCpus=1
should_transfer_files=YES
when_to_transfer_output=ON_EXIT_OR_EVICT
transfer_input_files=/home/prayag/coffeafcc/coffea-fcc-analyses/development/Batch/job_0.py,/home/prayag/coffeafcc/coffea-fcc-analyses/development/processor_mHrecoil.py
transfer_output_files=singularity.log.job_0,mHrecoil_mumu.coffea
output=out-0.$(ClusterId).$(ProcId)
error=err-0.$(ClusterId).$(ProcId)
log=log-0.$(ClusterId).$(ProcId)
queue 1