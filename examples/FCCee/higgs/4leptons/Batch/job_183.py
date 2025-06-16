
from coffea import util
from coffea.nanoevents import FCC
import os
from coffea.dataset_tools import apply_to_fileset,max_chunks
import dask
from processor import Fourleptons

dataset_runnable = {'p8_ee_WW_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_172110833.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '342e1eda-8ed6-11ed-b429-813b8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_127855974.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '32951b32-8ed6-11ed-8eed-0b398e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_040373155.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '312c8668-8ed6-11ed-9e62-30388e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_082774568.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '2f227ab2-8ed6-11ed-a847-46388e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_060727365.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '2fd0f0ba-8ed6-11ed-9e62-45398e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_189177636.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '30082eb8-8ed6-11ed-9e62-183a8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_191198998.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '301e3ac8-8ed6-11ed-9e62-6b3b8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_054129002.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '30f88f98-8ed6-11ed-bae6-5a398e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_000005189.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '30bd5072-8ed6-11ed-9e62-5e398e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_145598048.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '2ffd4dfe-8ed6-11ed-9e62-783d8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_007364771.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '300ddf7a-8ed6-11ed-9e62-ad388e80beef'}}, 'form': None, 'metadata': None}}
maxchunks = 10

to_compute = apply_to_fileset(
            Fourleptons(*[],**{}),
            max_chunks(dataset_runnable, maxchunks),
            schemaclass=FCC.get_schema('latest'),
            uproot_options={"filter_name": lambda x : "PARAMETERS" not in x}
)
computed = dask.compute(to_compute)
(Output,) = computed

print("Saving the output to : " , "4leptons-chunk183.coffea")
util.save(output= Output, filename="4leptons-chunk183.coffea")
print("File 4leptons-chunk183.coffea saved")
print("Execution completed.")

        