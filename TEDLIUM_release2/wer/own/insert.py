import difflib

# 替换为你的路径
with open("reftext.txt", "r", encoding="utf-8") as f:
    reference_lines = f.readlines()

with open("asrfinal_lower.txt", "r", encoding="utf-8") as f:
    baseline_lines = f.readlines()

# 统一长度（建议提前确保对齐）
min_len = min(len(reference_lines), len(baseline_lines))
reference_lines = reference_lines[:min_len]
baseline_lines = baseline_lines[:min_len]

# 初始化统计计数和错误样例
subs, ins, dels, hits = 0, 0, 0, 0
sub_examples, ins_examples, del_examples, hit_examples = [], [], [], []

for idx, (ref, hyp) in enumerate(zip(reference_lines, baseline_lines)):
    ref_words = ref.strip().split()
    hyp_words = hyp.strip().split()
    sm = difflib.SequenceMatcher(None, ref_words, hyp_words)
    
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            hits += (i2 - i1)
            hit_examples.append((ref_words[i1:i2], hyp_words[j1:j2], idx))
        elif tag == 'replace':
            subs += max(i2 - i1, j2 - j1)
            sub_examples.append((ref_words[i1:i2], hyp_words[j1:j2], idx))
        elif tag == 'insert':
            ins += (j2 - j1)
            ins_examples.append(([], hyp_words[j1:j2], idx))
        elif tag == 'delete':
            dels += (i2 - i1)
            del_examples.append((ref_words[i1:i2], [], idx))

# 打印统计信息
print(f"Substitutions（替换）: {subs}")
print(f"Insertions（插入）: {ins}")
print(f"Deletions（删除）: {dels}")
print(f"Hits（完全匹配）: {hits}")

# 输出每类前5个例子（可扩展）
print("\n--- 替换 示例 ---")
for r, h, idx in sub_examples[:5]:
    print(f"[Line {idx+1}] REF: {' '.join(r)} | HYP: {' '.join(h)}")

print("\n--- 插入 示例 ---")
for r, h, idx in ins_examples[:5]:
    print(f"[Line {idx+1}] INSERTED: {' '.join(h)}")

print("\n--- 删除 示例 ---")
for r, h, idx in del_examples[:5]:
    print(f"[Line {idx+1}] DELETED: {' '.join(r)}")

print("\n--- 匹配 示例 ---")
for r, h, idx in hit_examples[:5]:
    print(f"[Line {idx+1}] MATCHED: {' '.join(r)}")
