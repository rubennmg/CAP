sbatch --wrap="python3 mul_benchmark.py" \
  --job-name=mul_benchmark \
  --output=logs/phase2_3/big_mul_benchmark_2_3_$(date +%Y-%m-%d_%H-%M-%S).log \
  --error=logs/phase2_3/big_mul_benchmark_2_3_error_$(date +%Y-%m-%d_%H-%M-%S).log \
  --nodes=1 \
  --ntasks=1
