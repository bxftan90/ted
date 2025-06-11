from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio
import os
import torch

# configure
model_id = "facebook/wav2vec2-base-100h"
audio_dir = "./test_segments"
output_path = "wav2vec2_baseline_results.txt"

# Loading Models
processor = Wav2Vec2Processor.from_pretrained(model_id)
model = Wav2Vec2ForCTC.from_pretrained(model_id)
model.eval()

# batch file
results = {}
for fname in sorted(os.listdir(audio_dir)):
    if not fname.endswith(".wav"):
        continue
    path = os.path.join(audio_dir, fname)
    speech, sr = torchaudio.load(path)

    # If not 16kHz, resample
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
        speech = resampler(speech)

    # feed into model
    input_values = processor(speech.squeeze(), return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        logits = model(input_values).logits
        pred_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(pred_ids[0])

    results[fname] = transcription.lower()

# Save Recognition Results
with open(output_path, "w") as f:
    for fname, text in results.items():
        f.write(f"{fname}: {text}\n")

print(f"Reasoning is complete and the results have been saved to {output_path}")
