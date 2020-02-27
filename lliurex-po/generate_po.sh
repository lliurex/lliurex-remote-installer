#!/bin/bash

PYTHON_FILES="../lliurex-remote-installer-gui.install/usr/share/lliurex-remote-installer/*.py"
UI_FILES="../lliurex-remote-installer-gui.install/usr/share/lliurex-remote-installer/lliurex-remote-installer.ui"
INDICATOR_FILE="../lliurex-remote-installer-indicator.install/usr/bin/lliurex-remote-installer-indicator"

mkdir -p lliurex-remote-installer-gui/

xgettext $UI_FILES $PYTHON_FILES -o lliurex-remote-installer-gui/lliurex-remote-installer-gui.pot
xgettext --join-existing -L python $INDICATOR_FILE -o lliurex-remote-installer-gui/lliurex-remote-installer-gui.pot



