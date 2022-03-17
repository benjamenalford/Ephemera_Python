#!/usr/bin/env bash

echo "createing Ephemera service ..."
chmod 755 ../ephemera.py
cp ephemera.sh /etc/init.d/ephemera
cp ephemera.service /etc/systemd/system
chmod +x /etc/init.d/ephemera

echo "created the ephemera service"