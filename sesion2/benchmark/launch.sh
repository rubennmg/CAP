sbatch --wrap="python3 mul_benchmark.py" \
  --job-name=mul_benchmark \
  --output=logs/big_mul_benchmark_2_$(date +%Y-%m-%d_%H-%M-%S).log \
  --error=logs/big_mul_benchmark_2-error_$(date +%Y-%m-%d_%H-%M-%S).log \
  --time=08:00:00 \
  --nodes=1 \
  --ntasks=1
