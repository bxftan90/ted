import re
import pandas as pd

# Load ref and hyp texts
with open("/scratch/s5836670/TEDLIUM_release2/wer/own/asrfinal_lower.txt", "r", encoding="utf-8") as f:
    ref_text = f.read().lower()

with open("/scratch/s5836670/TEDLIUM_release2/wer/own/reftext.txt", "r", encoding="utf-8") as f:
    hyp_text = f.read().lower()

# Helper: tokenize as words
def tokenize(text):
    return re.findall(r"\b\w+\b", text)

ref_tokens = tokenize(ref_text)
hyp_tokens = tokenize(hyp_text)

# Detect possible connected words in hyp (length > 8 and not in ref)
joined_hyp_tokens = [w for w in set(hyp_tokens) if len(w) > 8 and w not in ref_tokens]

# Try to split each into two known words in REF that also appear consecutively
valid_splits = []

for word in joined_hyp_tokens:
    for i in range(3, len(word)-2):
        left = word[:i]
        right = word[i:]
        # check both left and right exist and appear consecutively in ref
        if left in ref_tokens and right in ref_tokens:
            for j in range(len(ref_tokens) - 1):
                if ref_tokens[j] == left and ref_tokens[j+1] == right:
                    valid_splits.append((word, f"{left} {right}"))
                    break

# Convert to DataFrame for display
df = pd.DataFrame(valid_splits, columns=["Recognized Result", "Correct Form"])
import ace_tools as tools; tools.display_dataframe_to_user(name="Valid Connected Word Errors", dataframe=df)

