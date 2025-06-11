import os
import re

def extract_words_from_stm(folder):
    words = set()
    for filename in os.listdir(folder):
        if filename.endswith(".stm"):
            with open(os.path.join(folder, filename), 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    text = ' '.join(parts[6:])
                    tokens = re.findall(r'\b\w+\b', text.lower())
                    words.update(tokens)
    return words

train_words = extract_words_from_stm("train/stm")
test_words = extract_words_from_stm("test/stm")

oov_words = {w for w in test_words if w not in train_words}
print(f"find {len(oov_words)}  OOV：", list(oov_words)[:20])

with open("OOV_words.txt", "w") as f:
    for word in sorted(oov_words):
        f.write(word + "\n")
print("Saved to OOV_words.txt")
