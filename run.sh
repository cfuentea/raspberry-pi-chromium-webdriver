docker run --rm -w /tmp -v /home/raspb/produccion/raspberry-pi-chromium-webdriver:/tmp -h $(hostname) cfuentealba/chromium-arm64:latest python3 test.py
