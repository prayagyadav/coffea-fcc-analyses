
from coffea import util
from coffea.nanoevents import BaseSchema
import os
from coffea.dataset_tools import apply_to_fileset,max_chunks
import dask
from processor import example_processor

dataset_runnable = {'p8_ee_ZH_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_002125352.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e03206c0-aa66-11eb-b728-24478e80beef'}}, 'form': None, 'metadata': None}, 'p8_ee_ZZ_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZZ_ecm240/events_000203378.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '5796bdea-cb1e-11ec-bfa9-3369b9bcbeef'}}, 'form': None, 'metadata': None}}
maxchunks = 10

to_compute = apply_to_fileset(
            example_processor(*[],**{}),
            max_chunks(dataset_runnable, maxchunks),
            schemaclass=BaseSchema,
)
computed = dask.compute(to_compute)
(Output,) = computed

print("Saving the output to : " , "Example.coffea")
util.save(output= Output, filename="Example.coffea")
print("File Example.coffea saved")
print("Execution completed.")

        