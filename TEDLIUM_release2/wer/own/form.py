from jiwer import compute_measures, compose, RemovePunctuation, ToLowerCase, RemoveMultipleSpaces, Strip

# 读取文件
with open("reftext.txt", "r", encoding="utf-8") as f:
    ref = f.read()

with open("asrfinal_lower (1).txt", "r", encoding="utf-8") as f:
    hyp = f.read()

# 文本预处理
transform = compose([
    RemovePunctuation(),
    ToLowerCase(),
    RemoveMultipleSpaces(),
    Strip()
])

# 计算详细对齐信息
measures = compute_measures(ref, hyp, truth_transform=transform, hypothesis_transform=transform)
alignment = measures["alignment"]

# 分类错误
substitutions = []
insertions = []
deletions = []

for op, ref_word, hyp_word in alignment:
    if op == "substitution" and len(substitutions) < 10:
        substitutions.append((ref_word, hyp_word))
    elif op == "insertion" and len(insertions) < 10:
        insertions.append(("", hyp_word))
    elif op == "deletion" and len(deletions) < 10:
        deletions.append((ref_word, ""))

# 打印表格形式
print("=== Substitution Errors ===")
print("{:<20} {:<20}".format("REF (Correct)", "HYP (ASR Output)"))
for r, h in substitutions:
    print("{:<20} {:<20}".format(r, h))

print("\n=== Insertion Errors ===")
print("{:<20} {:<20}".format("REF (Correct)", "HYP (ASR Output)"))
for r, h in insertions:
    print("{:<20} {:<20}".format(r, h))

print("\n=== Deletion Errors ===")
print("{:<20} {:<20}".format("REF (Correct)", "HYP (ASR Output)"))
for r, h in deletions:
    print("{:<20} {:<20}".format(r, h))
