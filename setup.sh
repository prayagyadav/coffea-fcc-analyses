if [ "${0}" != "${BASH_SOURCE}" ]; then
	# Determinig the location of this setup script
	export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

	export PYTHONPATH="${LOCAL_DIR}/scripts:${PYTHONPATH}"
	alias coffea-fcc-analyses="${LOCAL_DIR}/bin/coffea-fcc-analyses"
fi

# Install plugins
cd ${LOCAL_DIR}/scripts/plugins
plugins=("fastjet")

# Loop through the array
for plugin in "${plugins[@]}"
do
    echo "Installing $plugin ..."
    cd $plugin
    make
    cd ..
done

cd ${LOCAL_DIR}
