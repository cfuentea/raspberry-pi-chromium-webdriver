Docker image to run Python Selenium with Chromium on Raspberry Pi

# Usage
1. Install Docker on Raspberry Pi (Guia de oficial de instalación)[https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/]
2. Clone this repo
3. Test the image by running the command:
```
docker run --rm -w /tmp -v $(pwd):/tmp cfuentealba/chromium-arm64:0.1 python3 test.py
```
