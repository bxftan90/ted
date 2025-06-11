import re

# 替换规则：将连接的单词还原为两个词
custom_mappings = {
    "andhow": "and how",
    "andatferst": "and at first",
    "don’t": "do not",
    "everam": "ever am",
    "gaveme": "gave me",
    "howaryou’regoing": "how are you’re going",
    "it’s": "it is",
    "itdoesn’t": "it doesn’t",
    "itwas": "it was",
    "nearto": "near to",
    "ofcourse": "of course",
    "thankyou": "thank you",
    "thatyou": "that you",
    "you’re": "you are",
    "youknow": "you know"
}

def normalize_text(text, mappings):
    # 替换连接词组
    for wrong, correct in mappings.items():
        text = text.replace(wrong, correct)
    # 转小写、去标点
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()

def calculate_wer(ref, hyp):
    # Levenshtein距离计算WER
    r_len = len(ref)
    d = [[0] * (len(hyp) + 1) for _ in range(r_len + 1)]
    for i in range(r_len + 1):
        d[i][0] = i
    for j in range(len(hyp) + 1):
        d[0][j] = j
    for i in range(1, r_len + 1):
        for j in range(1, len(hyp) + 1):
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,     # 删除
                d[i][j - 1] + 1,     # 插入
                d[i - 1][j - 1] + cost  # 替换
            )
    return d[-1][-1] / r_len

def main():
    # 路径可修改为你的文件位置
    ref_path = "/scratch/s5836670/TEDLIUM_release2/wer/own/reftext.txt"
    hyp_path = "/scratch/s5836670/TEDLIUM_release2/wer/own/asrfinal_lower.txt"

    with open(ref_path, "r", encoding="utf-8") as f:
        ref_text = f.read()
    with open(hyp_path, "r", encoding="utf-8") as f:
        hyp_text = f.read()

    # 文本标准化
    ref_words = normalize_text(ref_text, {})  # ref不替换
    hyp_words = normalize_text(hyp_text, custom_mappings)

    # 计算 WER
    wer = calculate_wer(ref_words, hyp_words)
    print(f"WER: {wer:.4f}")

if __name__ == "__main__":
    main()
