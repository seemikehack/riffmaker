RiffMaker
=========

RiffMaker transforms text input into musical phrases. You specify the scale
that notes should be taken from and the key for the riff, and RiffMaker maps
the characters in the text input to intervals in your chosen scale.

# Running

The included Dockerfile simplifies running RiffMaker.

1. `docker build -t riffmaker .`
2. `docker run -it riffmaker`
