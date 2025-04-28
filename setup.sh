if [ "${0}" != "${BASH_SOURCE}" ]; then
  # Determinig the location of this setup script
  export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

  export PYTHONPATH="${LOCAL_DIR}/scripts:${PYTHONPATH}"
  alias coffea-fcc-analyses="${LOCAL_DIR}/bin/coffea-fcc-analyses"

  # Plugin stuff ...
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(python -c 'import fastjet; print(fastjet.__path__[0])')/_fastjet_core/lib
fi
