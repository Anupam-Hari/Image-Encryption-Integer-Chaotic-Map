import time
import psutil
import os
import statistics
import tracemalloc

from analysis.security_metrics.quality import compute_psnr, compute_ssim
from analysis.security_metrics.entropy import compute_entropy
from analysis.security_metrics.correlation import (
    horizontal_correlation,
    vertical_correlation,
    diagonal_correlation
)
from analysis.security_metrics.differential import compute_npcr, compute_uaci
from analysis.security_metrics.chi_square import compute_chi_square

import matplotlib.pyplot as plt


# ---------------------------------------------------------
# PLOTTING UTILITIES
# ---------------------------------------------------------

def _plot_histogram_comparison(original, encrypted):
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.hist(original.flatten(), bins=256)
    plt.title("Original Histogram")

    plt.subplot(1, 2, 2)
    plt.hist(encrypted.flatten(), bins=256)
    plt.title("Encrypted Histogram")

    plt.tight_layout()
    plt.show()


def _plot_correlation_comparison(original, encrypted, direction):

    def get_xy(image, direction):
        if direction == "horizontal":
            x = image[:, :-1].flatten()
            y = image[:, 1:].flatten()
        elif direction == "vertical":
            x = image[:-1, :].flatten()
            y = image[1:, :].flatten()
        elif direction == "diagonal":
            x = image[:-1, :-1].flatten()
            y = image[1:, 1:].flatten()
        else:
            raise ValueError("Invalid direction")

        return x[:5000], y[:5000]

    x1, y1 = get_xy(original, direction)
    x2, y2 = get_xy(encrypted, direction)

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.scatter(x1, y1, s=1)
    plt.title(f"Original {direction.capitalize()} Correlation")

    plt.subplot(1, 2, 2)
    plt.scatter(x2, y2, s=1)
    plt.title(f"Encrypted {direction.capitalize()} Correlation")

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# SECURITY EVALUATION
# ---------------------------------------------------------

def evaluate_security(original, encrypted, encrypted_modified=None, plot=False):

    results = {}

    # Numerical Metrics
    results["PSNR"] = compute_psnr(original, encrypted)
    results["SSIM"] = compute_ssim(original, encrypted)
    results["Entropy"] = compute_entropy(encrypted)

    results["Corr_H"] = horizontal_correlation(encrypted)
    results["Corr_V"] = vertical_correlation(encrypted)
    results["Corr_D"] = diagonal_correlation(encrypted)

    chi_val, p_val = compute_chi_square(encrypted)
    results["ChiSquare"] = chi_val
    results["Chi_p"] = p_val

    if encrypted_modified is not None:
        results["NPCR"] = compute_npcr(encrypted, encrypted_modified)
        results["UACI"] = compute_uaci(encrypted, encrypted_modified)

    # Plot only if explicitly requested
    if plot:
        _plot_histogram_comparison(original, encrypted)
        _plot_correlation_comparison(original, encrypted, "horizontal")
        _plot_correlation_comparison(original, encrypted, "vertical")
        _plot_correlation_comparison(original, encrypted, "diagonal")

    return results


# ---------------------------------------------------------
# COMPUTATIONAL EVALUATION
# ---------------------------------------------------------

def evaluate_computation(original, encrypt_function, num_runs=1):

    results = {}

    process = psutil.Process(os.getpid())

    size_bytes = original.nbytes
    num_pixels = original.size

    # Warm-up
    encrypt_function(original)
    process.cpu_percent(interval=None)

    wall_times = []
    cpu_times = []
    cpu_percents = []

    for _ in range(num_runs):
        t_wall_start = time.perf_counter()
        t_cpu_start = time.process_time()

        encrypt_function(original)

        t_cpu_end = time.process_time()
        t_wall_end = time.perf_counter()

        wall_times.append(t_wall_end - t_wall_start)
        cpu_times.append(t_cpu_end - t_cpu_start)
        cpu_percents.append(process.cpu_percent(interval=None))

    # Memory measurement
    tracemalloc.start()
    encrypt_function(original)
    mem_current, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Latency
    mean_wall = statistics.mean(wall_times)
    mean_cpu = statistics.mean(cpu_times)

    results["Latency_mean_s"] = mean_wall
    results["Latency_std_s"] = statistics.stdev(wall_times) if num_runs > 1 else 0.0
    results["Latency_min_s"] = min(wall_times)
    results["Latency_max_s"] = max(wall_times)

    # CPU
    results["CPU_time_mean_s"] = mean_cpu
    results["CPU_efficiency"] = mean_cpu / mean_wall if mean_wall > 0 else 0.0

    # Throughput
    results["Encryptions_per_sec"] = 1.0 / mean_wall
    results["FPS"] = results["Encryptions_per_sec"]
    results["Throughput_MBps"] = (size_bytes / (1024 * 1024)) / mean_wall
    results["Throughput_Mpps"] = (num_pixels / 1_000_000) / mean_wall

    # CPU %
    results["CPU_percent_mean"] = statistics.mean(cpu_percents)
    results["CPU_percent_max"] = max(cpu_percents)

    if results["CPU_percent_mean"] > 0:
        results["Efficiency_MB_per_CPU_pct"] = (
            results["Throughput_MBps"] / results["CPU_percent_mean"]
        )

    results["Energy_Index"] = results["CPU_percent_mean"] * mean_wall

    results["Memory_current_KB"] = mem_current / 1024
    results["Memory_peak_KB"] = mem_peak / 1024

    return results


# ---------------------------------------------------------
# MASTER EVALUATION
# ---------------------------------------------------------

def evaluate(original, encrypted, encrypt_function,
             encrypted_modified=None, num_runs=10, plot=False):

    security = evaluate_security(
        original,
        encrypted,
        encrypted_modified,
        plot=False
    )

    computation = evaluate_computation(
        original,
        encrypt_function,
        num_runs
    )

    return {**security, **computation}