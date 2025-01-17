# Getting Started

## Installation

Start with cloning the repository

``` bash
   git clone https://github.com/prayagyadav/coffea-fcc-analyses.git
```

## Dependencies
Access to `LXPLUS` is a recommended requirement. This is because, `Singularity` containers for `COFFEA` are available in `LXPLUS` through `/cvmfs`. Locally, one can install `COFFEA` through `pip`, `conda` or download a `docker` or `singularity` container. If installed locally, one should ensure the `Python` version used be `< 3.13.0`.

## Requirements

1. Access to `/cvmfs`
2. Access to `/eos`
3. To have read access to the `FCC` pre-generated samples, one needs to be
   subscribed to the following `e-group` (with the owner's approval):
   `fcc-eos-access`

## Workflow

A. Clone the `coffea-fcc-analyses` repository,
```bash
git clone https://github.com/prayagyadav/coffea-fcc-analyses.git
```

B. Move into the cloned directory,
``` bash
cd coffea-fcc-analyses
```

C. Set up all the environment variables with sourcing `setup.sh`,
```bash
source setup.sh
```

D. Start a singularity shell containing `COFFEA-2025.1.0` with
``` bash
./shell
```
One can also call a version other than the default with:
``` bash
./shell coffeateam/<name of the desired container>
```
A full list of all the available `COFFEA` containers are at `/cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/`.

(Please note that `coffea-fcc-analysis` is only compatible with containers with `COFFEA version >= 2024.10.0`)

One can also modify `shell` for personalized workflows by editing it. The current contents of
`shell` are :

``` bash

   #!/usr/bin/env bash

   if [ "$1" == "" ]; then
       export COFFEA_IMAGE=coffeateam/coffea-dask-almalinux8:2025.1.0-py3.12
   else
       export COFFEA_IMAGE=$1
   fi

   echo "Coffea Image: ${COFFEA_IMAGE}"

   EXTERNAL_BIND=${PWD}

   singularity exec -B /etc/condor -B /eos -B /afs -B /cvmfs --pwd ${PWD} \
       /cvmfs/unpacked.cern.ch/registry.hub.docker.com/${COFFEA_IMAGE} \
       /bin/bash --rcfile /srv/.bashrc
```
