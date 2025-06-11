import os

input_dir = "/scratch/s5836670/TEDLIUM_release2/test/stm"
output_file = "/scratch/s5836670/TEDLIUM_release2/test/stm_combined.txt"

with open(output_file, "w", encoding="utf-8") as outfile:
    for fname in sorted(os.listdir(input_dir)):
        if fname.endswith(".stm"):
            fpath = os.path.join(input_dir, fname)
            with open(fpath, "r", encoding="utf-8") as infile:
                lines = infile.readlines()
                outfile.writelines(lines)

print(f"combine done：{output_file}")
