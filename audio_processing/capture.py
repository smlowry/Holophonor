import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
BUFFER_SIZE = 2048
DEVICE_INDEX = 3
VOLUME_THRESHOLD = 0.002

last_note = None

def hz_to_note(freq):
    if freq <= 0:
        return None
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    midi = int(round(69 + 12 * np.log2(freq / 440.0)))
    name = note_names[midi % 12]
    octave = midi // 12 - 1
    return f"{name}{octave}"

def detect_pitch_autocorr(signal, sr):
    """Estimate pitch using autocorrelation (works better for bass)."""
    # Normalize
    signal = signal - np.mean(signal)
    corr = np.correlate(signal, signal, mode="full")
    corr = corr[len(corr)//2:]

    # Find first minimum (ignore zero lag)
    d = np.diff(corr)
    start = np.nonzero(d > 0)[0]
    if len(start) == 0:
        return 0
    start = start[0]

    # Peak after first minimum
    peak = np.argmax(corr[start:]) + start
    if peak == 0:
        return 0
    return sr / peak

def audio_callback(indata, frames, time, status):
    global last_note
    if status:
        print("Status:", status)

    audio = indata.mean(axis=1)
    rms = np.sqrt(np.mean(audio**2))

    if rms < VOLUME_THRESHOLD:
        return

    pitch = detect_pitch_autocorr(audio, SAMPLE_RATE)
    note = hz_to_note(pitch)

    if note and note != last_note:
        print(note)
        last_note = note

def main():
    try:
        with sd.InputStream(device=DEVICE_INDEX,
                            callback=audio_callback,
                            channels=2,
                            samplerate=SAMPLE_RATE,
                            blocksize=BUFFER_SIZE):
            print("Listening... press Ctrl+C to stop.")
            while True:
                pass
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    main()
