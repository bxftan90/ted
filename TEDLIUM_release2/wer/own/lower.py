input_path = "/scratch/s5836670/TEDLIUM_release2/wer/own/asrfinal.txt"
output_path = "/scratch/s5836670/TEDLIUM_release2/wer/own/asrfinal_lower.txt"

with open(input_path, "r") as infile, open(output_path, "w") as outfile:
    for line in infile:
        outfile.write(line.lower())
