# ukutuner
This is a basic Python script that uses a short-term Fast Fourier Transform to detect the GCEA tuning chords of a standard ukulele.
Run the script, wait a second, and strum a chord. The base note should appear right next to the "note" label. From there, tune it until the number on
the right is +-.02 away from 0. Happy strumming!

## Modules Required
numpy
pyAudio

## What's next?
I'm working on making a UI that visualizes how far the note is from where you want it to be so you don't have to look at the command line is all day.
Also, this will be turned into an object that can perform several functions(general tuning, watching for one note, adjusting NOTE_MIN and NOTE_MAX for guitars, bass, banjo, etc.)
and pushed as a module on PyPi so you can insert a tuner within your app!
