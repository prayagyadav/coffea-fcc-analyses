
from coffea import util
from coffea.nanoevents import BaseSchema, FCC #fix import of FCC on condor
import os
from coffea.dataset_tools import apply_to_fileset,max_chunks
import dask
from processor import jetclustering

dataset_runnable = {'wzp6_ee_mumuH_Hbb_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_Hbb_ecm240/events_159112833.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f24b1152-8e72-11ed-8419-8f398e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_Hbb_ecm240/events_160156697.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f599a2d8-8e72-11ed-b264-1c388e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_Hbb_ecm240/events_008395310.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f395cdcc-8e72-11ed-bae4-853d8e80beef'}}, 'form': None, 'metadata': None}}
maxchunks = 10

to_compute = apply_to_fileset(
            jetclustering(*[],**{}),
            max_chunks(dataset_runnable, maxchunks),
            schemaclass=<class 'scripts.schema.fcc.FCCSchema'>,
)
computed = dask.compute(to_compute)
(Output,) = computed

print("Saving the output to : " , "jetclustering.coffea")
util.save(output= Output, filename="jetclustering.coffea")
print("File jetclustering.coffea saved")
print("Execution completed.")

        