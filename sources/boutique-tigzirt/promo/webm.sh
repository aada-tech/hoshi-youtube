#!/bin/sh
# Pour le rendu sous Linux : recode vid/*.mp4 en VP9 (une image clé par image, seek exact) dans vid/*.webm.
# usage : FFMPEG_BIN=ffmpeg sh webm.sh   puis   PROMO_VID_EXT=webm python3 render.py ...
cd "$(dirname "$0")/vid" || exit 1
for f in *.mp4; do "${FFMPEG_BIN:-ffmpeg}" -y -loglevel error -i "$f" -an -c:v libvpx-vp9 -crf 14 -b:v 0 -g 1 -pix_fmt yuv420p -row-mt 1 "${f%.mp4}.webm"; done
