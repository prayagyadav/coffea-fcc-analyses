#!/bin/bash

# Run everything in a virtual environment for maximum compatibility
python3 -m venv temp_env
source temp_env/bin/activate

pip3 install fastjet

swig -version

# Set flags and locations
FASTJET_LOC=$(python3 -c "import fastjet; print(fastjet.__path__[0])")
 
INCS="-I${FASTJET_LOC}/_fastjet_core/include/"
 
# Start building
set -e  # Exit if any command fails
 
# Run SWIG to generate wrapper
swig -c++ -python ${INCS} -o Recombiner_wrap.cxx Recombiner.i
 
echo "Wrapper Generated."

# Delete the virtual environment
deactivate
rm -rf temp_env

