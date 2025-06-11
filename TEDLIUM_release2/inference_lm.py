import os
import torch
import torchaudio
import soundfile as sf
import multiprocessing as mp
mp.set_start_method("spawn", force=True)

from transformers import Wav2Vec2ProcessorWithLM, Wav2Vec2ForCTC

# Set the cache path to avoid writing to home3
os.environ["TRANSFORMERS_CACHE"] = "/scratch/s5836670/huggingface"
os.environ["HF_HOME"] = "/scratch/s5836670/huggingface"
os.environ["PYCTCDECODE_CACHE"] = "/scratch/s5836670/huggingface/pyctcdecode"

# path
model_id = "patrickvonplaten/wav2vec2-base-100h-with-lm"
audio_dir = "/scratch/s5836670/TEDLIUM_release2/test_segments"
output_file = "/scratch/s5836670/TEDLIUM_release2/wav2vec2_with_lm_results.txt"

print("CUDA available:", torch.cuda.is_available())
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Loading models and processors
processor = Wav2Vec2ProcessorWithLM.from_pretrained(model_id)
model = Wav2Vec2ForCTC.from_pretrained(model_id).to(device)
model.eval()

# inference function
def transcribe(path):
    # Load audio and force it to float32
    speech_array, sr = sf.read(path, dtype='float32')
    if len(speech_array) == 0:
        raise ValueError("Audio is empty.")

    # forced mono
    if speech_array.ndim > 1:
        speech_array = speech_array.mean(axis=1)

    # change over to tensor
    speech_tensor = torch.tensor(speech_array)

    # resample
    if sr != 16000:
        speech_tensor = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(speech_tensor)

    # input model
    input_values = processor(speech_tensor.numpy(), sampling_rate=16000, return_tensors="pt").input_values.to(device)

    with torch.no_grad():
        logits = model(input_values).logits  # shape: [1, time, vocab]

    # Decode logits with processor decoder with LM (no argmax required)
    predicted_text = processor.batch_decode(logits.cpu().numpy()).text[0]
    return predicted_text.lower()


    

# Batch Audio Processing
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w") as out_f:
    for fname in sorted(os.listdir(audio_dir)):
        if not fname.endswith(".wav"):
            continue
        fpath = os.path.join(audio_dir, fname)
        try:
            result = transcribe(fpath)
        except Exception as e:
            result = "[ERROR]"
            print(f"Error with {fname}: {e}")
        out_f.write(f"{fname}: {result}\n")
        print(f"{fname}: {result}")
