#!/bin/bash

 # Set flags and locations
 FLAGS="-fPIC"
 FASTJET_LOC=$(python3 -c "import fastjet; print(fastjet.__path__[0])")

 INCS="-I${FASTJET_LOC}/_fastjet_core/include/"
 LIBS="${FASTJET_LOC}/_fastjet_core/lib/libfastjet.so"
 PYTHONI=$(python3-config --includes)
 PYTHONL="-Xlinker -export-dynamic"

 for COMPILER in $(which -a g++ | uniq); do
   echo "Trying compiler: $COMPILER"

   $COMPILER ${FLAGS} ${INCS} -c Recombiner.cc -o Recombiner.o &> /dev/null
   if [ $? -ne 0 ]; then
     echo "Failed to compile Recombiner.cc with: $COMPILER"
     continue
   fi

   $COMPILER ${FLAGS} ${PYTHONI} ${INCS} -c Recombiner_wrap.cxx -o Recombiner_wrap.o &> /dev/null
   if [ $? -ne 0 ]; then
     echo "Failed to compile Recombiner_wrap.cxx with: $COMPILER"
     continue
   fi

   $COMPILER ${PYTHONL} ${FLAGS} ${INCS} -shared Recombiner.o Recombiner_wrap.o ${LIBS} -o _Recombiner.so &> /dev/null
   if [ $? -eq 0 ]; then
     echo "Compilation succeeded with: $COMPILER"
     exit 0
   else
     echo "Linking failed with: $COMPILER"
   fi
 done

 echo "All available g++ compilers failed!"
 exit 1
