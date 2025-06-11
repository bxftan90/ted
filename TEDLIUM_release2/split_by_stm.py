import os
from pydub import AudioSegment

wav_dir = "/scratch/s5836670/TEDLIUM_release2/test_wav"
stm_dir = "/scratch/s5836670/TEDLIUM_release2/test/stm"
output_dir = "./test_segments"
os.makedirs(output_dir, exist_ok=True)

for stm_file in os.listdir(stm_dir):
    if not stm_file.endswith(".stm"):
        continue
    base_name = stm_file.replace(".stm", "")
    wav_path = os.path.join(wav_dir, base_name + ".wav")
    if not os.path.exists(wav_path):
        continue

    audio = AudioSegment.from_wav(wav_path)

    with open(os.path.join(stm_dir, stm_file), 'r') as f:
        for i, line in enumerate(f):
            parts = line.strip().split()
            if len(parts) < 7:
                continue
            start_time = float(parts[3]) * 1000
            end_time = float(parts[4]) * 1000
            segment_audio = audio[start_time:end_time]
            segment_filename = f"{base_name}_{i:04d}.wav"
            segment_path = os.path.join(output_dir, segment_filename)
            segment_audio.export(segment_path, format="wav")

print("Sentence-level audio clips have been saved to ./test_segments/")
