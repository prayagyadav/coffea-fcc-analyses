
from coffea import util
from coffea.nanoevents import BaseSchema
import os
from coffea.dataset_tools import apply_to_fileset,max_chunks
import dask
from processor_mHrecoil import mHrecoil

dataset_runnable = {'p8_ee_ZZ_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZZ_ecm240/events_000203378.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '5796bdea-cb1e-11ec-bfa9-3369b9bcbeef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZZ_ecm240/events_001062578.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '65fcbd2a-cb1a-11ec-a7a1-0b3b8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZZ_ecm240/events_001109319.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '0ad0919a-aa7a-11eb-9c26-2e518e80beef'}}, 'form': None, 'metadata': None}, 'p8_ee_WW_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_WW_ecm240/events_002446962.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '91790b62-aa7c-11eb-91e4-b8468e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_WW_ecm240/events_003660780.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'c0f764e2-aa7c-11eb-bbd6-f7448e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_WW_ecm240/events_003871346.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'c686d032-aa7c-11eb-b4b9-b4448e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_WW_ecm240/events_006111023.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '46429654-aa7c-11eb-a284-9d468e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_WW_ecm240/events_006917088.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '22bd26f4-aa7c-11eb-a04f-814c8e80beef'}}, 'form': None, 'metadata': None}, 'p8_ee_ZH_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_002125352.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e03206c0-aa66-11eb-b728-24478e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_004864728.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'df4890c6-aa66-11eb-af5e-464b8e80beef'}}, 'form': None, 'metadata': None}}
maxchunks = 10

to_compute = apply_to_fileset(
            mHrecoil(*[],**{'ecm': 240.0}),
            max_chunks(dataset_runnable, maxchunks),
            schemaclass=BaseSchema,
)
computed = dask.compute(to_compute)
(Output,) = computed

print("Saving the output to : " , "mHrecoil_mumu.coffea")
util.save(output= Output, filename="mHrecoil_mumu.coffea")
print("File mHrecoil_mumu.coffea saved")
print("Execution completed.")

        