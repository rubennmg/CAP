sbatch --wrap="./1-multiply_matrices 1024 1024 128" \
  --job-name=1-multiply_matrices \
  --output=test_$(date +%Y-%m-%d_%H-%M-%S).log \
  --error=test_$(date +%Y-%m-%d_%H-%M-%S).log \
  --time=08:00:00 \
  --nodes=1 \
  --ntasks=1
