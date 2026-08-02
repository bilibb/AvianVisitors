#!/usr/bin/env bash

if [ "$EUID" == 0 ]
  then echo "Please run as a non-root user."
  exit
fi

if [ "$(uname -m)" != "aarch64" ] && [ "$(uname -m)" != "x86_64" ];then
  echo "BirdNET-Pi requires a 64-bit OS.
It looks like your operating system is using $(uname -m),
but would need to be aarch64."
  exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info[0]}{sys.version_info[1]}')")
if [ "${PY_VERSION}" == "39" ] ;then
  echo "### BirdNET-Pi requires a newer OS. Bullseye is deprecated, please use Bookworm. ###"
  [ -z "${FORCE_BULLSEYE}" ] && exit
fi

# we require passwordless sudo
sudo -K
if ! sudo -n true; then
    echo "Passwordless sudo is not working. Aborting"
    exit
fi

# Simple new installer
HOME=$HOME
USER=$USER

export HOME=$HOME
export USER=$USER

PACKAGES_MISSING=
for cmd in git jq ; do
  if ! which $cmd &> /dev/null;then
      PACKAGES_MISSING="${PACKAGES_MISSING} $cmd"
  fi
done
if [[ ! -z $PACKAGES_MISSING ]] ; then
  sudo apt update
  sudo apt -y install $PACKAGES_MISSING
fi

branch=german-dashboard

DATABASE_LANG=de
LATITUDE=52.2799
LONGITUDE=8.0471

git clone -b $branch --depth=1 https://github.com/bilibb/AvianVisitors.git ${HOME}/BirdNET-Pi &&

CONF_TEMPLATE="$HOME/BirdNET-Pi/scripts/install_config.sh"
sed -i "s/^DATABASE_LANG=en\$/DATABASE_LANG=$DATABASE_LANG/" "$CONF_TEMPLATE"
sed -i "s/^LATITUDE=\$LATITUDE\$/LATITUDE=$LATITUDE/" "$CONF_TEMPLATE"
sed -i "s/^LONGITUDE=\$LONGITUDE\$/LONGITUDE=$LONGITUDE/" "$CONF_TEMPLATE"

# Patch homepage to German if DATABASE_LANG=de
if [ "$DATABASE_LANG" = "de" ]; then
  python3 "$HOME/BirdNET-Pi/avian/patch_homepage_de.py" \
          "$HOME/BirdNET-Pi/avian/frontend"
fi

$HOME/BirdNET-Pi/scripts/install_birdnet.sh
if [ ${PIPESTATUS[0]} -eq 0 ];then
  echo "Installation completed successfully"
  sudo reboot
else
  echo "The installation exited unsuccessfully."
  exit 1
fi
