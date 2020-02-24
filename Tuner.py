import pyaudio
import numpy
import scipy as sp
import math
notes = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']
RATE=44100
RECORD_SECONDS = 1
CHUNKSIZE = 1024	
# initialize portaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE)
while True:
    #Gets Data:
    frames = [] # A python-list of chunks(numpy.ndarray)
    for _ in range(0, int(RATE / CHUNKSIZE * RECORD_SECONDS)):
        data = stream.read(CHUNKSIZE)
        frames.append(numpy.frombuffer(data, dtype=numpy.int16))
    #Convert the list of numpy-arrays into a 1D array (column-wise)
    numpydata = numpy.hstack(frames)
    #fftw	
    #Performs FFT on array
    fftData = numpy.fft.fft(numpydata)
    #Gets length of sample for data
    fftDataLen = len(fftData)/2

    #Dominant freqnecy:

    freqs = numpy.fft.fftfreq(len(fftData))
    idx = numpy.argmax(numpy.abs(fftData))
    freq = freqs[idx]
    #print( abs(freq * RATE))
    
    note = notes[int(round(12.0*(math.log(abs(freq/440.0), 2))+5)%12)]
    noteNu = int(round(12*(math.log(abs(freq/440.0), 2)))) + 234
    ifreq = abs(freq * RATE)
    tfreq = 2**((noteNu - 49)/12) *440.0
    dfreq = (tfreq/100)*6
    diff = ((ifreq - tfreq)/dfreq)*10
    if(diff > 0):
        l = 0
        d = int(diff)
    else:
        d = 0
        l = int(diff)
    print("{:>5}".format(">"*l) + "{:^6}".format(note) + "{:<5}".format("<"*d))

# close stream
stream.stop_stream()
stream.close()
p.terminate()
