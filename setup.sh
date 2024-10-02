if [ "${0}" != "${BASH_SOURCE}" ]; then
	# Determinig the location of this setup script
	export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

	export PYTHONPATH="${LOCAL_DIR}/scripts:${PYTHONPATH}"
	alias coffea-fcc-analyses="${LOCAL_DIR}/bin/coffea-fcc-analyses"
fi
