#!/usr/bin/env bash
# Launcher for E001_example-baseline — reference example (illustrative).
# Smoke test must pass locally before queuing (compute-budget-policy).
set -euo pipefail

ID="E001_example-baseline"
CONFIG="configs/${ID}.yaml"
OUTDIR="results/${ID}"
mkdir -p "${OUTDIR}"

# #SBATCH --job-name=E001_example-baseline
# #SBATCH --partition=gpu
# #SBATCH --gres=gpu:1
# #SBATCH --time=02:00:00
# #SBATCH --output=results/E001_example-baseline/slurm-%j.out

# module load cuda/12.4
# conda activate example-proj

python scripts/capture_environment.py --out "${OUTDIR}/env.json" || true

if [ "${SMOKE:-0}" = "1" ]; then
  echo "Smoke: 100-sample overfit on CPU..."
  python train.py --config "${CONFIG}" --smoke
  exit $?
fi

python train.py --config "${CONFIG}" --output "${OUTDIR}" --resume

# Hand-over: sbatch launchers/E001_example-baseline.sh ; paste back the job ID.
