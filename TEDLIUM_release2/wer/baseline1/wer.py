from jiwer import wer

# 读取参考和识别文本
with open("reftext.txt", "r") as f:
    reference = [line.strip() for line in f.readlines()]

with open("testtext.txt", "r") as f:
    hypothesis = [line.strip() for line in f.readlines()]

# 确保行数一致
assert len(reference) == len(hypothesis), "行数不一致，不能计算逐行WER"

# 计算逐行WER
wers = [wer(r, h) for r, h in zip(reference, hypothesis)]
average_wer = sum(wers) / len(wers)

print(f"平均 WER：{average_wer:.2%}")
