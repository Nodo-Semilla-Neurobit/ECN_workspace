#!/bin/bash
# Despliegue único de soberanía HID (requiere sudo UNA sola vez)
sudo cp 90-neurobit-hid.rules /etc/udev/rules.d/
sudo modprobe uinput
echo "uinput" | sudo tee /etc/modules-load.d/uinput.conf
sudo groupadd -f input
sudo usermod -aG input "$USER"
sudo udevadm control --reload-rules && sudo udevadm trigger
echo "[✓ UDEV] Reglas cristalizadas. Re-iniciá sesión para aplicar el grupo 'input'."

