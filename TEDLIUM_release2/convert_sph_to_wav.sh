for file in /scratch/s5836670/TEDLIUM_release2/test/sph/*.sph; do
    fname=$(basename "$file" .sph)
    sox "$file" -r 16000 -c 1 "test_wav/${fname}.wav"
done
