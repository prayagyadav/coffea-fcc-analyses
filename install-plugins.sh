if [ "${0}" != "${BASH_SOURCE}" ]; then
	# Determinig the location of this setup script
	export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

	export PYTHONPATH="${LOCAL_DIR}/scripts:${PYTHONPATH}"
	alias coffea-fcc-analyses="${LOCAL_DIR}/bin/coffea-fcc-analyses"
fi


# As a note, remember to have the build time dependencies on your system
# For fastjet they are :
#   For Deb : sudo apt-get update && sudo apt-get install -y libboost-dev libmpfr-dev libgmp-dev swig autoconf libtool
#   For RHEL: sudo dnf install boost-devel mpfr-devel gmp-devel swig autoconf libtool python3-devel

# List of required Python dependencies
REQUIRED_PACKAGES=("fastjet")

check_and_install_package() {
    package=$1
    if ! python3 -c "import ${package}" &> /dev/null; then
        echo "${package} is not installed. Installing..."
        pip3 install "$package"
    else
        echo "${package} is already installed."
    fi
}

echo "Installing dependencies ..."
# Check and install each package
for package in "${REQUIRED_PACKAGES[@]}"; do
    check_and_install_package "$package"
done



# Temporarily install swig within the container
# cd /tmp
# wget https://github.com/swig/swig/archive/refs/tags/v4.1.1.tar.gz
# tar -xzf v4.1.1.tar.gz
# cd swig-4.1.1

# ./autogen.sh
# ./configure --prefix=$HOME/.local
# make -j$(nproc)
# make install

# Now make sure $HOME/.local/bin is in your PATH:
# export PATH=$HOME/.local/bin:$PATH


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

echo "Installed all the dependencies successfully."
