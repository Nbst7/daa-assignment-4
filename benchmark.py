import csv
import random
import statistics
import time

from Python.source.algorithms import naive, kmp, rk
algorithms = {
    "naive": naive,
    "kmp": kmp,
    "rk": rk,
}
sizes = [
    (300, 10),
    (1000, 30),
    (3000, 100),
]
rows = []
for case in ["random", "repetitive"]:
    for n, m in sizes:
        seed = 42
        rng = random.Random(seed)
        if case == "random":
            alphabet = "abcd"
            text = "".join(rng.choices(alphabet, k=n))
            pattern = "".join(rng.choices(alphabet, k=m))
        else:
            text = "a" * n
            pattern = "a" * (m - 1) + "b"
        request = {
            "text": text,
            "pattern": pattern,
        }
        expected = naive(request)["positions"]
        for name, algorithm in algorithms.items():
            assert algorithm(request)["positions"] == expected
            algorithm(request)
            times = []
            for _ in range(3):
                start = time.perf_counter()
                result = algorithm(request)
                elapsed = (
                    time.perf_counter() - start
                ) * 1000
                assert result["positions"] == expected
                times.append(elapsed)
            median = statistics.median(times)
            rows.append([
                case, n, m, seed, name,
                *[round(t, 4) for t in times],
                round(median, 4), "YES"
            ])
            print(
                f"{case:10} n={n:4} m={m:3} "
                f"{name:5} median={median:.4f} ms"
            )
with open(
    "benchmark_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.writer(file)
    writer.writerow([
        "Case", "n", "m", "Seed", "Algorithm",
        "Run 1 (ms)", "Run 2 (ms)", "Run 3 (ms)",
        "Median (ms)", "Correct outputs checked"
    ])
    writer.writerows(rows)
print("\nAll benchmarks completed!")
print("Results saved to benchmark_results.csv")