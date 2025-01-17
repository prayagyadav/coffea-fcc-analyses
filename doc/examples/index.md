# Examples

## Structure of Examples

A typical `coffea-fcc-analyses` project is separated into these files:
- config.py
- processor\_.py
- runner\_.py
- plotter\_.py

## Setup

A. Clone the `coffea-fcc-analyses` repository,
```bash
git clone https://github.com/prayagyadav/coffea-fcc-analyses.git
```

B. Move into the cloned directory,
``` bash
cd coffea-fcc-analyses
```

C. Set up all the environment variables with sourcing `setup.sh`,
```bash
source setup.sh
```

D. Start a singularity shell with COFFEA-2025 with
``` bash
./shell
```
One can also call a version other than the default with:
``` bash
./shell coffeateam/<name of the desired container>
```
A full list of all the available COFFEA containers are at `/cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/`.

(Please note that `coffea-fcc-analysis` is only compatible with containers with COFFEA version >= 2024.10.0)


## List of examples :

### FCC-ee
- Higgs
   - mHrecoil
      - [mHrecoil_mumu](./examples/FCCee/higgs/mHrecoil/mumu/mHrecoil_mumu.md)
