<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/prayagyadav/coffea-fcc-analyses/refs/heads/main/doc/_static/coffea-fcc-analyses-logo-inverted.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/prayagyadav/coffea-fcc-analyses/refs/heads/main/doc/_static/coffea-fcc-analyses-logo.png">
  <img alt="COFFEA-FCC-Analyses-logo" src="https://raw.githubusercontent.com/prayagyadav/coffea-fcc-analyses/refs/heads/main/doc/_static/coffea-fcc-analyses-logo.png">
</picture>

# COFFEA FCC Analyses

COFFEA-FCC-Analyses is an analysis framework for the Future Circular Collider samples, based on [COFFEA](https://coffea-hep.readthedocs.io/en/latest/). It provides simplified workflows to start an FCC analysis with minimal boilerplate code.

Check out the latest documentation at [https://coffea-fcc-analyses.readthedocs.io/en/latest/index.html](https://coffea-fcc-analyses.readthedocs.io/en/latest/index.html).

___
## Quick start

1. Clone this repository

```bash
    git clone https://github.com/prayagyadav/coffea-fcc-analyses.git
```

2. Before starting each session, setup the environment variables with setup.sh

```bash
    source setup.sh
```

3. If using on lxplus (Recommended), start a singularity session with shell

```bash
    ./shell
```

4. Install extra plugins with install-plugins.sh

```bash
    source install-plugins.sh
```
If using a singularity container on lxplus (Recommended), run the installation script from within the container.
```bash
    ./shell
    singularity>
    singularity> source install-plugins.sh
```

---

## Start a new project

1. Create a new project from templates (lets call the project 'test')

```bash
    coffea-fcc-analyses init test
```

2. A new folder named 'test' is created

```bash
    ls test
```
```bash
      config.py  plotter.py  processor.py  runner.py
```
3. Modify the config and processor as per your needs. plotter and runner could be kept as they are. To run the analysis with dask:
```bash
    ./shell
    shell> python runner.py -e dask
```
or condor with
```bash
    shell> python runner.py -e condor
```
4. Make plots with plotter:
```bash
    shell> python plotter.py
```


## Examples

1. Find out working examples in the `examples` directory

2. Jupyter notebook demonstrations of the same examples can be found in the `notebooks` directory

---
## People
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/prayagyadav"><img src="https://avatars.githubusercontent.com/u/122809705?v=4" width="100px;" alt="Prayag Yadav"/><br /><sub><b>Prayag Yadav</b></sub></a><br /></td>
       <td align="center" valign="top" width="14.28%"><a href="https://github.com/davidlange6"><img src="https://avatars.githubusercontent.com/u/5042883?v=4" width="100px;" alt="David Lange"/><br /><sub><b>David Lange</b></sub></a><br /></td>
       <td align="center" valign="top" width="14.28%"><a href="https://github.com/gomber"><img src="https://avatars.githubusercontent.com/u/5593325?v=4" width="100px;" alt="Bhawna Gomber"/><br /><sub><b>Bhawna Gomber</b></sub></a><br /></td>
    </tr>
  </tbody>
</table>

---
Support for this work was provided by HSF-India - NSF
