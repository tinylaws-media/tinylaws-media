#!/bin/sh
# Mixage final : voix nettoyée + bruitages (sous la voix) + musique (sous la voix, creusée dans les médiums) -> mix.wav à -14 LUFS
# usage : sh mix.sh [gain_musique] [gain_bruitages]
GM=${1:-0.22}; GS=${2:-1.6}; V=../audio/voix_propre.wav
ffmpeg -v error -y -i $V -i sfx.wav -i music.wav -filter_complex "\
[0]aformat=sample_rates=48000:channel_layouts=mono,apad=whole_dur=83,asplit=3[v][k1][k2];\
[1]volume=$GS[s];[s][k1]sidechaincompress=threshold=0.015:ratio=10:attack=8:release=300,alimiter=limit=0.2:attack=2:release=80:level=false,aformat=channel_layouts=stereo[sd];\
[2]volume=$GM,equalizer=f=2500:t=q:w=1:g=-5,equalizer=f=300:t=q:w=1:g=-2[m];[k2]aformat=channel_layouts=stereo[k2s];[m][k2s]sidechaincompress=threshold=0.02:ratio=3:attack=40:release=700[md];\
[v]aformat=channel_layouts=stereo[vs];[vs][sd][md]amix=inputs=3:normalize=0:duration=first,atrim=0:83,loudnorm=I=-14:TP=-1.5:LRA=9,aformat=sample_rates=48000" mix.wav
