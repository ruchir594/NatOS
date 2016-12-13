#!/bin/bash

echo “Recording… Press Ctrl+C to Stop.”
arecord -D “plughw:1,0” -q -f cd -t wav | ffmpeg -loglevel panic -y -i – -ar 16000 -acodec flac file.flac > /dev/null 2>&1

echo “Processing…”
wget -q -U “Mozilla/5.0” –post-file file.flac –header “Content-Type: audio/x-flac; rate=16000” -O – “http://www.google.com/speech-api/v1/recognize?lang=en-us&client=chromium” | cut -d” -f12 >stt.txt

echo -n “You Said: ”
cat stt.txt

rm file.flac > /dev/null 2>&1
