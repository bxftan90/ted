# *Improving OOV Word Recognition in End-to-End ASR via Lightweight Domain Adaptation with a TED-LIUM2 N-gram Language Model*

---

## Overview

This project investigates the effectiveness of integrating a lightweight, domain-adapted n-gram language model to improve the recognition of out-of-vocabulary (OOV) words in end-to-end ASR systems.  
The experiments focus on TED-LIUM2 speech data and aim to enhance transcription accuracy in spontaneous speech conditions.

The base ASR model used is [`facebook/wav2vec2-base-100h`](https://huggingface.co/facebook/wav2vec2-base-100h), with decoding support using a 4-gram language model trained using KenLM.

---

## Requirements & Environment

All experiments were conducted on the **Hábrók High-Performance Computing (HPC) Cluster** at the University of Groningen:

- **GPU**: NVIDIA A100 (40GB VRAM)  
- **CPU**: 20 cores  
- **Memory**: 48GB  

This configuration enabled efficient batch inference, decoding, and large-scale evaluation with no memory bottlenecks.

---

## Directory Overview

The key file structure and main components are summarized below:
```
TEDLIUM_release2/
├── trainingdataset/                  # Cleaned training text for LM training
│   ├── dev_stm_cleaned.txt           # Clean dev STM text
│   └── train_stm_onlytext.txt        # Clean train STM text
│
├── wer/                              # Word error rate computation framework
│   ├── baseline1/                    # Baseline ASR evaluation
│   │   ├── reftext.txt
│   │   ├── testtext.txt
│   │   ├── insert.py                 # Error type counter
│   │   └── wer.py                    # WER computation
│   │
│   ├── baselinelm/                   # Inference + WER using baseline LM
│   └── own/                          # Inference + WER using domain-adapted LM
│       ├── asrfinal.txt / .lower.txt # ASR outputs before/after normalization
│       ├── reftext.txt               # Gold reference transcription
│       ├── clean2_include477.py      # Removes connect errors before WER calc
│       ├── insert.py, wer.py         # Detailed WER and error count tools
│       ├── clean.py, form.py, lower.py
│       └── check_space_words.py      # Custom error analysis on space issues
│
├── combine_stm.py                    # Merges STM for training
├── convert_sph_to_wav.sh             # Shell script to convert SPH to WAV
├── inference_lm.py                   # Inference using LM decoding
├── inference_nlm.py                  # Inference without LM
├── inference_own.py                  # Inference using own TED-LIUM2-trained LM
├── oov.py                            # OOV term extraction and tracking
├── OOV_words.txt                     # List of extracted OOV terms
├── split_by_stm.py                   # Audio segmentation by STM
├── wav2vec2_baseline_results.txt     # WER for baseline (no LM)
├── wav2vec2_with_lm_results.txt      # WER for baseline with LM
│
├── 4grams.py                         # Modify lm_4gram.arpa to add and output fixed LM
├── lm_4gram_corrected_fixed.arpa     # Trained ARPA LM (text)
└── lm_4gram_corrected.binary         # Compiled KenLM binary (for decoding)
```

---

## Language Model Details

The 4-gram language model was trained using [KenLM](https://github.com/kpu/kenlm), based on guidance from the Hugging Face tutorial:  [Boosting Wav2Vec2 with n-grams in Transformers (Colab)](https://colab.research.google.com/github/patrickvonplaten/notebooks/blob/master/Boosting_Wav2Vec2_with_n_grams_in_Transformers.ipynb)

- **Corpus**: Cleaned transcripts from [TED-LIUM2](https://www.openslr.org/19/)  
- **Format**: All `.sph` audio was manually converted to `.wav`  
- **Test setup**: Long test audios were segmented into **30-second chunks** for evaluation

---

## AI Contribution Statement

This project involved the use of ChatGPT-4o (OpenAI) for:

- Generating and fixong Python scripts
All AI-generated code was manually reviewed and modified as needed to ensure correctness.

---

## Acknowledgements

This work is part of the MSc Voice Technology program and made possible by the **Hábrók HPC cluster** at the University of Groningen.  
Special thanks to the open-source tools used:  
[KenLM](https://github.com/kpu/kenlm), [Transformers](https://huggingface.co/docs/transformers/index), and [OpenSLR](https://www.openslr.org/19/)

---


