#!/bin/bash

set -e

# Create swapfile of 1GB with block size 1MB
dd if=/dev/zero of=/swapfile bs=1024 count=1048576

# Set up the swap file
mkswap /swapfile

# Enable swap file immediately
swapon /swapfile

# Enable swap file on every boot
echo '/swapfile          swap            swap    defaults        0 0' >> /etc/fstab

apt-get update

apt-get install -y tmux

apt-get install -y redis-server # not used yet, will be used for Celery
apt-get install -y python3
apt-get install -y python3-dev # To compile python C extensions
apt-get install -y pylint
apt-get install -y python-pip
pip install virtualenvwrapper

exec sudo -i -u vagrant /bin/bash - <<'AS_VAGRANT'

RCFILE=~/.bash_profile

cat <<'EOS' >> $RCFILE
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh

# Automaically load virtual env on `cd` to directory.
# https://gist.github.com/clneagu/7990272
check_virtualenv() {
    if [ -e .venv ]; then
        env=`cat .venv`
        if [ "$env" != "${VIRTUAL_ENV##*/}" ]; then
            echo "Found .venv in directory. Calling: workon ${env}"
            workon $env
        fi
    fi
}
venv_cd () {
    builtin cd "$@" && check_virtualenv
}
check_virtualenv
alias cd="venv_cd"
EOS

source $RCFILE
export VIRTUALENV_PYTHON=/usr/bin/python3

APPPATH=~/tttoe
VENVNAME=`cat $APPPATH/.venv`
mkvirtualenv -r $APPPATH/requirements.txt $VENVNAME

AS_VAGRANT
