#!/bin/sh

mkdir -p $HOME/.config/bardshell
cp config/bard.toml $HOME/.config/bardshell/

pip install bardapi toml --break-system-packages
