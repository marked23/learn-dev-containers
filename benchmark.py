"""
CPU (NumPy) vs GPU (PyTorch) matrix multiplication benchmark.

Shows the speedup you get from running on a GPU inside this dev container.
Interrogates hardware to report detailed system info alongside results.
"""

import time
import numpy as np
import torch

SIZES = [1024, 2048, 4096, 8192]
ROUNDS = 5
WARMUP = 5


def get_cpu_name():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return "Unknown"


def get_system_ram_gb():
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if "MemTotal" in line:
                    return int(line.split()[1]) / 1024 / 1024
    except OSError:
        pass
    return 0.0


def get_numpy_blas():
    """Return the BLAS library NumPy is linked against."""
    try:
        info = np.show_config(mode="dicts")
        blas = info.get("Build Dependencies", {}).get("blas", {})
        name = blas.get("name", "unknown")
        version = blas.get("version", "")
        config = blas.get("openblas configuration", "")
        return name, version, config
    except Exception:
        return "unknown", "", ""


def get_gpu_info():
    """Collect detailed GPU information."""
    props = torch.cuda.get_device_properties(0)
    vram_gb = props.total_memory / (1024 ** 3)

    # Determine backend
    hip = getattr(torch.version, "hip", None)
    cuda = getattr(torch.version, "cuda", None)
    if hip:
        backend = f"ROCm/HIP {hip.split('-')[0]}"
    elif cuda:
        backend = f"CUDA {cuda}"
    else:
        backend = "Unknown"

    # GPU architecture
    arch = getattr(props, "gcnArchName", None)
    if not arch:
        arch = f"SM {props.major}.{props.minor}"

    gpu_type = "Integrated (shared system memory)" if props.is_integrated else "Discrete (dedicated VRAM)"

    return {
        "name": props.name,
        "type": gpu_type,
        "is_integrated": props.is_integrated,
        "memory_gb": vram_gb,
        "arch": arch,
        "compute_units": props.multi_processor_count,
        "backend": backend,
        "pytorch": torch.__version__,
    }


def print_system_info():
    gpu = get_gpu_info()
    cpu = get_cpu_name()
    ram = get_system_ram_gb()
    blas_name, blas_ver, blas_config = get_numpy_blas()

    mem_label = "Shared RAM" if gpu["is_integrated"] else "VRAM"

    print("=" * 60)
    print("  SYSTEM INFO")
    print("=" * 60)
    print(f"  CPU          : {cpu}")
    print(f"  System RAM   : {ram:.1f} GB")
    print(f"  GPU          : {gpu['name']}")
    print(f"  GPU Type     : {gpu['type']}")
    print(f"  GPU Arch     : {gpu['arch']}")
    print(f"  {mem_label:13s}: {gpu['memory_gb']:.1f} GB")
    print(f"  Compute Units: {gpu['compute_units']}")
    print(f"  Backend      : {gpu['backend']}")
    print(f"  PyTorch      : {gpu['pytorch']}")
    blas_label = blas_name
    if blas_ver:
        blas_label += f" {blas_ver}"
    print(f"  NumPy BLAS   : {blas_label}")
    print("=" * 60)


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


print_system_info()
print()
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
