#!/bin/bash
 
 # Set flags and locations
 FLAGS="-fPIC"
 FASTJET_LOC=$(python3 -c "import fastjet; print(fastjet.__path__[0])")
 
 INCS="-I${FASTJET_LOC}/_fastjet_core/include/"
 LIBS="${FASTJET_LOC}/_fastjet_core/lib/libfastjet.so"
 PYTHONI=$(python3-config --includes)
 PYTHONL="-Xlinker -export-dynamic"
 
 # Start building
 set -e  # Exit if any command fails
 
 # Compile Recombiner.cc
 g++ ${FLAGS} ${INCS} -c Recombiner.cc -o Recombiner.o
 
 # Compile the SWIG wrapper
 g++ ${FLAGS} ${PYTHONI} ${INCS} -c Recombiner_wrap.cxx -o Recombiner_wrap.o
 
 # Link everything into a shared object
 g++ ${PYTHONL} ${FLAGS} ${INCS} -shared Recombiner.o Recombiner_wrap.o ${LIBS} -o _Recombiner.so
 
 echo "Build completed successfully!"
