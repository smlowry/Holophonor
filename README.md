# Holophonor

🎼 **Phase 1: Live Instrument → Note Detection**

This project is an early prototype of a modern *Holophonor* — inspired by Futurama.  
Right now, the pipeline captures audio from an instrument (bass via AudioBox USB 96) and detects the **note names in real time**.

---

## ✅ Current Progress
- Audio interface input working (AudioBox USB 96)
- Real-time audio capture via `sounddevice`
- Pitch detection using **autocorrelation** (optimized for bass)
- Note names (`E1`, `A1`, `D2`, etc.) printed to the console when plucked
- Noise floor suppressed via RMS threshold

---

## 📂 Project Structure
