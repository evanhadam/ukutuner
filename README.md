# ukutuner
This is a basic Python script that uses a short-term Fast Fourier Transform to detect the GCEA tuning chords of a standard ukulele.
Run the script, wait a second, and strum a chord. The base note should appear right next to the "note" label. From there, tune it until the number on
the right is +-.02 away from 0. Happy strumming!

## Modules Required
numpy, pyAudio

## Under Construction
- UI Implimentation to be able to see wavelengths of noise and how far it is from the tuned note
- Adjusting min and max note to make the program compatible for bass, guitar, banjo, etc.
- Turning this from a script to callable functions and uploading as a module to PyPi
