# 🎹 Jazz Piano Music Generator using GPT

This project explores the use of GPT-based transformer models for generating jazz-style piano music. By treating symbolic MIDI data as a sequential language, we train a transformer to compose harmonically rich and improvisationally expressive jazz piano sequences.

---

## 📌 Overview

Transformer-based language models, especially GPT, have revolutionized sequence modeling. This project applies GPT's autoregressive capabilities to music generation using MIDI data transformed into piano-roll formats. The result: AI-generated jazz piano compositions that exhibit realistic polyphony and stylistic coherence.

---

## 🧠 Features

- GPT-based architecture for symbolic music generation  
- Input: MIDI jazz piano dataset (Doug McKenzie collection)  
- Preprocessing: Piano-roll binary matrices at 32 steps/sec  
- Tokenization: Multi-hot pitch encoding  
- Output: AI-generated MIDI jazz tracks

---

## 📂 Dataset

We use the [Doug McKenzie Jazz Piano MIDI Dataset](http://www.midkar.com/jazz/jazz.html) consisting of ~200 jazz piano tracks.

**Preprocessing steps:**

- Isolate piano track by note count  
- Transpose all tracks to C Major / A Minor  
- Convert to piano-roll matrices (128 pitches × time)  
- Discard velocity and reduce to binary note on/off values

---

## 🏗️ Model Architecture

- Decoder-only GPT  
- Positional encoding (sinusoidal)  
- Multi-head self-attention  
- Categorical cross-entropy loss  
- Sequence length: 1500  
- Implemented in TensorFlow

---

## 🏋️‍♀️ Training

- **Epochs**: 300  
- **Batch size**: 32  
- **Optimizer**: Adam  
- **Loss function**: Categorical cross-entropy  
- **Framework**: TensorFlow  
- **Generation**: Autoregressive sampling + MIDI reconstruction using [PrettyMIDI](https://github.com/craffel/pretty-midi)

---

## 🎧 Results

### Objective Evaluation

- **Unique pitches**: 79  
- **Pitch class diversity**: 12  
- **Polyphony score**: 215  
- **Zero empty-bar rate**: ~0%

### Subjective Evaluation

Generated outputs reflect:
- Rich harmonic content  
- Rhythmic variation  
- Stylistic resemblance to authentic jazz improvisation

---

## ⚠️ Limitations & Future Work

- No expressive timing or dynamics due to binary encoding  
- Limited dataset size  
- Potential enhancements:
  - Include velocity and tempo encoding  
  - Expand dataset with diverse genres  
  - Conditional generation on chord progressions

## 🧑‍💻 Authors

- **Hiba Ammar** – Latakia University  
- **Mayyar Saied** – Latakia University


