
from coffea import util
from coffea.nanoevents import FCC
import os
from coffea.dataset_tools import apply_to_fileset,max_chunks
import dask
from processor import Fourleptons

dataset_runnable = {'p8_ee_WW_ecm240': {'files': {'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_002241019.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '00f67468-ad17-11ed-92c4-433b8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_115669735.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f772a786-ad16-11ed-bdab-5f3a8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_055586488.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f7a31e0c-ad16-11ed-97bf-50808e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_142702162.root': {'object_path': 'events', 'steps': [[0, 37728]], 'num_entries': 37728, 'uuid': 'f7ee2db6-ad16-11ed-97bf-45c38e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_008671922.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'fc59ca22-ad16-11ed-a3da-76c38e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_101306566.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f725e9d2-ad16-11ed-bdab-1d3f8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_078567640.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': '013a8f7c-ad17-11ed-ae1c-913d8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_111747831.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f76cb89e-ad16-11ed-97bf-30398e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_100461538.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f7ae18d4-ad16-11ed-97bf-483f8e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_079988542.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'f7ced380-ad16-11ed-97bf-cec08e80beef'}, 'root://eospublic.cern.ch:1094//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_WW_ecm240/events_019991573.root': {'object_path': 'events', 'steps': [[0, 50000], [50000, 100000]], 'num_entries': 100000, 'uuid': 'fa344862-ad16-11ed-ab26-d7c08e80beef'}}, 'form': None, 'metadata': None}}
maxchunks = 10

to_compute = apply_to_fileset(
            Fourleptons(*[],**{}),
            max_chunks(dataset_runnable, maxchunks),
            schemaclass=FCC.get_schema('latest'),
            uproot_options={"filter_name": lambda x : "PARAMETERS" not in x}
)
computed = dask.compute(to_compute)
(Output,) = computed

print("Saving the output to : " , "4leptons-chunk229.coffea")
util.save(output= Output, filename="4leptons-chunk229.coffea")
print("File 4leptons-chunk229.coffea saved")
print("Execution completed.")

        