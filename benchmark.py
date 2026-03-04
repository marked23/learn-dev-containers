"""
CPU (NumPy) vs GPU (PyTorch ROCm) matrix multiplication benchmark.

Shows the speedup you get from running on the AMD APU via ROCm
inside this dev container.
"""

import time
import numpy as np
import torch

SIZES = [1024, 2048, 4096, 8192]
ROUNDS = 5
WARMUP = 5


def benchmark_numpy(n, rounds):
    a = np.random.randn(n, n).astype(np.float32)
    b = np.random.randn(n, n).astype(np.float32)
    start = time.perf_counter()
    for _ in range(rounds):
        _ = a @ b
    elapsed = time.perf_counter() - start
    return elapsed / rounds


def benchmark_pytorch_gpu(n, rounds):
    a = torch.randn(n, n, device="cuda")
    b = torch.randn(n, n, device="cuda")
    torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(rounds):
        _ = a @ b
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    return elapsed / rounds


print(f"Device: {torch.cuda.get_device_name(0)}")
print(f"Rounds per size: {ROUNDS}")
print(f"{'Size':>6}  {'NumPy (CPU)':>12}  {'PyTorch (GPU)':>14}  {'Speedup':>8}")
print("-" * 50)

# Warmup the GPU so first timed run isn't penalized
for _ in range(WARMUP):
    a = torch.randn(1024, 1024, device="cuda")
    _ = a @ a
    torch.cuda.synchronize()

for n in SIZES:
    t_np = benchmark_numpy(n, ROUNDS)
    t_pt = benchmark_pytorch_gpu(n, ROUNDS)
    speedup = t_np / t_pt
    print(f"{n:>6}  {t_np:>10.4f} s  {t_pt:>12.4f} s  {speedup:>7.1f}x")
