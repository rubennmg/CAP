sbatch --wrap="python3 mul_benchmark.py" \
  --job-name=mul_benchmark \
  --output=logs/phase1/big_mul_benchmark_1_$(date +%Y-%m-%d_%H-%M-%S).log \
  --error=logs/phase1/big_mul_benchmark_1_-error_$(date +%Y-%m-%d_%H-%M-%S).log \
  --nodes=1 \
  --ntasks=1
