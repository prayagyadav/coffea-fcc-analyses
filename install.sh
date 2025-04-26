if [ "${0}" != "${BASH_SOURCE}" ]; then
	# Determinig the location of this setup script
	export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

	export PYTHONPATH="${LOCAL_DIR}/scripts:${PYTHONPATH}"
	alias coffea-fcc-analyses="${LOCAL_DIR}/bin/coffea-fcc-analyses"
fi






# # List of required Python packages
# REQUIRED_PACKAGES=("coffea" "awkward" "numpy" "dask" "mplhep" "numba" "vector" "fastjet" "hist")

# check_and_install_package() {
#     package=$1
#     if ! python3 -c "import ${package}" &> /dev/null; then
#         echo "${package} is not installed. Installing..."
#         pip3 install "$package"
#     else
#         echo "${package} is already installed."
#     fi
# }

# # Check and install each package
# for package in "${REQUIRED_PACKAGES[@]}"; do
#     check_and_install_package "$package"
# done






# Install plugins
cd ${LOCAL_DIR}/scripts/plugins
plugins=("fastjet")

# Loop through the array
for plugin in "${plugins[@]}"
do
    echo "Installing Plugin: $plugin ..."
    cd $plugin
    bash build.sh
    cd ..
done

cd ${LOCAL_DIR}
