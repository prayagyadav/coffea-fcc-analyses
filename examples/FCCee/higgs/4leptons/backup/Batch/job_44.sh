#!/usr/bin/bash
export LOCAL_DIR=$(pwd)
export COFFEA_IMAGE_PATH=/cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-dask-almalinux8:2025.1.0-py3.12
echo "Coffea Image: ${COFFEA_IMAGE_PATH}"
EXTERNAL_BIND=${PWD}
echo $(pwd)
echo $(ls)
tar -xvf scripts.tar
singularity exec -B /etc/condor -B /eos -B /afs -B /cvmfs --pwd ${PWD} ${COFFEA_IMAGE_PATH} /usr/local/bin/python3 job_44.py -e dask >> singularity.log.job_44
echo $(ls)