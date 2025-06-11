import os
import gc
import torch
import soundfile as sf
from tqdm import tqdm
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from pyctcdecode import build_ctcdecoder

# path
lm_path = "/scratch/s5836670/lm_4gram_corrected.binary"
wav_dir = "/scratch/s5836670/TEDLIUM_release2/test_segments"
output_txt = "/scratch/s5836670/asr_result.txt"

# Setting up the device: use the CUDA GPU if it is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Loading processors and models
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-100h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-100h").to(device)
model.eval()

# Load Decoder
vocab_list = processor.tokenizer.convert_ids_to_tokens(list(range(processor.tokenizer.vocab_size)))
decoder = build_ctcdecoder(vocab_list, kenlm_model_path=lm_path)

# inference
with open(output_txt, "w") as fout:
    for fname in tqdm(sorted(os.listdir(wav_dir))):
        if not fname.endswith(".wav"):
            continue
        wav_path = os.path.join(wav_dir, fname)
        print(f"🔍 Processing: {fname}")
        try:
            speech, sr = sf.read(wav_path)
            if sr != 16000:
                print(f"Warning: skipping {fname}, not 16kHz")
                continue

            # inputs.input_values is automatically transferred to the GPU
            inputs = processor(speech, sampling_rate=sr, return_tensors="pt").to(device)

            with torch.no_grad():
                logits = model(inputs.input_values).logits[0].cpu().numpy()  # .cpu() 后转回 numpy 给 decoder

            text = decoder.decode(logits)
            fout.write(f"{fname}:\t{text}\n")

        except Exception as e:
            print(f"Error processing {fname}: {e}")
        finally:
            for var in ["inputs", "logits", "speech"]:
                if var in locals():
                    del locals()[var]
            gc.collect()
