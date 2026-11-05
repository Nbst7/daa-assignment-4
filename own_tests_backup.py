from Python.source.algorithms import naive, kmp, rk
tests = [
    ("overlapping", "aaaaa", "aaa", [0, 1, 2]),
    ("empty pattern", "abc", "", [0, 1, 2, 3]),
    ("long pattern", "ab", "abcd", []),
    ("collision", "abdj", "ab", [0]),
    ("case sensitive", "aAaA", "Aa", [1]),
]
algorithms = {
    "naive": naive,
    "kmp": kmp,
    "rk": rk,
}
for name, text, pattern, expected in tests:
    request = {"text": text, "pattern": pattern}
    for algorithm_name, algorithm in algorithms.items():
        actual = algorithm(request)["positions"]
        assert actual == expected, (
            f"FAIL {name} / {algorithm_name}: "
            f"expected {expected}, got {actual}"
        )
        print(f"PASS {name} / {algorithm_name}")
print("All 15 own tests passed!")