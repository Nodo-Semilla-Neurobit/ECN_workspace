#!/bin/bash
##NB::ORIENTACION::v0.1##
# Pip-Boy Neurobitrónico: leer el espacio físico + anunciar presencia radial.
cd "$(dirname "$0")/__MFN_Structure" || exit 1

# 1) Vista física (la que renderiza el S.O.) — solo como referencia.
tree -a > RegistroDePresencia.map

# 2) Anuncio de presencia (aún sin nombre definitivo: marca provisional).
TS=$(date +%Y%m%d_%H%M%S)
echo "└── az_S3:P2:B2__PRESENCIA_${TS} (anuncio: sin_id)" >> RegistroDePresencia.map

# 3) Vista lógica: brújula radial + camino al centro.
python3 ../neurobit_pipboy.py --estoy az:S3:P2:B2 --map RegistroDePresencia.map
