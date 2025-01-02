Installation
======

Dependencies:
-------------
A} Access to LXPLUS
   Singularity containers for COFFEA are available in LXPLUS through /cvmfs

B} Locally, one can install COFFEA through pip, conda or download a docker/singularity container

It is recommended that LXPLUS be used for all the analyses. If installed locally, one should ensure the Python version used in < 3.13.0.

Requirements:
-------------

1. Access to ``/cvmfs``
2. Access to ``/eos``
3. To have read access to the FCC pre-generated samples, one needs to be
   subscribed to the following e-group (with owner approval):
   ``fcc-eos-access``.

Workflow
--------

``coffea-fcc-analyses`` uses COFFEA 2024.9.0 with python 3.11 and dask
in an Almalinux 8 singularity container.

1. Clone the
   `coffea-fcc-analyses `__
   repository
2. ``cd coffea-fcc-analyses``
3. Set up the necessary environment variables by running
   ``./setup.sh``
3. The container shell could be started by executing ``./shell`` at
   the root of the
   `coffea-fcc-analyses `__
   repository.

One can also modify ``shell`` for personalized workflows by editing it. The current contents of
``shell`` are :

.. code:: bash

   #!/usr/bin/env bash

   if [ "$1" == "" ]; then
       export COFFEA_IMAGE=coffeateam/coffea-dask-almalinux8:2024.9.0-py3.11
   else
       export COFFEA_IMAGE=$1
   fi

   echo "Coffea Image: ${COFFEA_IMAGE}"

   EXTERNAL_BIND=${PWD}

   singularity exec -B /etc/condor -B /eos -B /afs -B /cvmfs --pwd ${PWD} \
       /cvmfs/unpacked.cern.ch/registry.hub.docker.com/${COFFEA_IMAGE} \
       /bin/bash --rcfile /srv/.bashrc
