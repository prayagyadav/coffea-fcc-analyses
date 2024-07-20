
from coffea import util
from coffea.nanoevents import BaseSchema
import os
from processor_mHrecoil import mHrecoil
from coffea.dataset_tools import apply_to_fileset,max_chunks
import dask

dataset_runnable = {'p8_ee_ZH_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_008903100.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e1c9821a-aa66-11eb-a7ee-18568e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_014692952.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'de59a7ae-aa66-11eb-828b-ee69b9bcbeef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_018575502.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'ddd1d252-aa66-11eb-9473-5ba18e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_022606167.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'de46981c-aa66-11eb-9d78-a5518e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_023301643.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e737600a-aa66-11eb-8e8e-c9548e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_025023196.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'db9bcb78-aa66-11eb-9d78-08578e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_029706955.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'dc553306-aa66-11eb-897b-c4518e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_031985013.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e325c75e-aa66-11eb-be7a-c4518e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_032939801.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e6e9e708-aa66-11eb-a35a-5d7b8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_034891952.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'df2d48de-aa66-11eb-af5e-664c8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_034912729.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'dc17e974-aa66-11eb-9d78-34518e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_037707607.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'ded6c220-aa66-11eb-bac3-6ea18e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_038855885.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f4391366-aa66-11eb-8612-5ca18e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_041407970.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'de957d06-aa66-11eb-9d78-b5548e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_043299326.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e85b4d5c-aa66-11eb-97b7-81508e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_045124915.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e64df848-aa66-11eb-8844-3a788e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_046318292.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'ed9a33c8-aa66-11eb-a623-5ca18e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_048296984.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'e4402de6-aa66-11eb-97b7-464b8e80beef'}}, 'form': None, 'metadata': None}}
maxchunks = 10

to_compute = apply_to_fileset(
            mHrecoil(),
            max_chunks(dataset_runnable, maxchunks),
            schemaclass=BaseSchema,
)
computed = dask.compute(to_compute)
(Output,) = computed

print("Saving the output to : " , "mHrecoil_mumu-chunk3.coffea")
util.save(output= Output, filename="mHrecoil_mumu-chunk3.coffea")
print("File mHrecoil_mumu-chunk3.coffea saved")# at outputs/FCCee/higgs/mH-recoil/mumu/")
print("Execution completed.")

        