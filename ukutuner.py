import numpy as np
import pyaudio
import time

NOTE_MIN = 60       # C4
NOTE_MAX = 69       # A4
FSAMP = 22050       # Sampling frequency(Hz)
FRAME_SIZE = 2048   # Samples per frame
FRAMES_PER_FFT = 32 # average across FRAMES_PER_FFT frames in FFT
SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT # SAMPLES_PER_FFT increases, frequency reads more accurately but takes longer
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT # frequency resolution

# low to high notes
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Music theory - converting frequencies to numbers that correlate with notes
# https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies

def freqNum(f): 
    return 69 + 12*np.log2(f/440.0)

def noteFftbin(n): 
    return numFreq(n)/FREQ_STEP

def numFreq(n): 
    return 440 * 2.0**((n-69)/12.0)

def noteName(n): 
    return NOTE_NAMES[n % 12] + str(n/12 - 1)

imin = max(0, int(np.floor(noteFftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(noteFftbin(NOTE_MAX+1))))

# stores samples
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=FSAMP, input=True, frames_per_buffer=FRAME_SIZE)
stream.start_stream()

# Hanning Window - helps cut down non-applicable local maxima and isolate our note frequency
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

curr_note_ind = 0
first = True
print('Detecting notes now!')

while stream.is_active() and curr_note_ind < 4:

    # shift buffer for space for new data
    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.frombuffer(stream.read(FRAME_SIZE), np.int16)

    # FFT w/ windowed buffer
    fft = np.fft.rfft(buf * window)

    # Frequency of most common response
    freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

    # Get note number, nearest note and their distance away from each other
    n = freqNum(freq)
    n0 = int(round(n))
    nDelta = n - n0

    num_frames += 1

    ukulele_notes = ['G', 'C', 'E', 'A']

    if first:
        print('Now tuning ' + ukulele_notes[curr_note_ind])
        first = False
        time.sleep(3)
    if num_frames >= FRAMES_PER_FFT:
        print('note: {:>3s} \t{:+.2f}'.format(noteName(n0), nDelta))
        if noteName(n0)[0] == ukulele_notes[curr_note_ind] and abs(nDelta) <= .03:
            print(ukulele_notes[curr_note_ind] + ' is in tune!')
            curr_note_ind += 1
            first = True
            time.sleep(1)
                
print('Your ukulele is in tune!')
time.sleep(10)