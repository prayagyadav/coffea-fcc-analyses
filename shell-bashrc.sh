#!/bin/bash

# Plugin exports
# 1. Fastjet
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(python -c 'import fastjet; print(fastjet.__path__[0])')/_fastjet_core/lib
