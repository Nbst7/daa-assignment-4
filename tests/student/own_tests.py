
import sys
from pathlib import Path

# Allow running this file from the project root
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Python.source.algorithms import (
    lcs, merge, tree, naive, kmp, rk, suffix, aho
)

passed = 0


def check(name, actual, expected):
    global passed
    assert actual == expected, (
        f"FAIL {name}: expected {expected}, got {actual}"
    )
    passed += 1
    print(f"PASS {name}")


# 1. LCS
check("lcs empty", lcs({"a": "", "b": "abc"}),
      {"length": 0, "sequence": ""})

check("lcs repeated", lcs({"a": "aaa", "b": "aa"}),
      {"length": 2, "sequence": "aa"})

check("lcs subsequence", lcs({"a": "abc", "b": "ac"}),
      {"length": 2, "sequence": "ac"})


# 2. MERGE
check("merge empty", merge({"sizes": []}),
      {"cost": 0, "plan": []})

check("merge one", merge({"sizes": [10]}),
      {"cost": 0, "plan": []})

check("merge two", merge({"sizes": [10, 20]}),
      {"cost": 30, "plan": [[0, 0, 1]]})

check("merge zeros", merge({"sizes": [0, 0, 0]})["cost"], 0)


# 3. TREE
check("tree empty",
      tree({"n": 0, "weights": [], "edges": []}),
      {"weight": 0, "selected": []})

check("tree negative",
      tree({"n": 2, "weights": [-5, -3],
            "edges": [[0, 1]]})["weight"], 0)

check("tree chain",
      tree({"n": 3, "weights": [5, 1, 5],
            "edges": [[0, 1], [1, 2]]})["weight"], 10)


# 4. NAIVE / KMP / RK
search_tests = [
    ("overlap", "aaaaa", "aaa", [0, 1, 2]),
    ("empty pattern", "abc", "", [0, 1, 2, 3]),
    ("both empty", "", "", [0]),
    ("long pattern", "ab", "abcd", []),
    ("collision", "abdj", "ab", [0]),
    ("case", "aAaA", "Aa", [1]),
    ("punctuation", "a!a!a", "!a", [1, 3]),
]

for name, text, pattern, expected in search_tests:
    request = {"text": text, "pattern": pattern}

    for algorithm_name, algorithm in [
        ("naive", naive), ("kmp", kmp), ("rk", rk)
    ]:
        check(
            f"{algorithm_name} {name}",
            algorithm(request)["positions"],
            expected
        )


# 5. SUFFIX ARRAY
check("suffix empty", suffix({"text": ""}),
      {"sa": [], "lcp": [], "repeated": ""})

check("suffix one", suffix({"text": "a"}),
      {"sa": [0], "lcp": [0], "repeated": ""})

check("suffix banana", suffix({"text": "banana"}),
      {"sa": [5, 3, 1, 0, 4, 2],
       "lcp": [0, 1, 3, 0, 0, 2],
       "repeated": "ana"})

check("suffix equal", suffix({"text": "aaaa"})["repeated"],
      "aaa")


# 6. AHO-CORASICK
check("aho empty dictionary",
      aho({"patterns": [], "texts": ["abc", ""]}),
      {"counts": [[], []]})

check("aho no texts",
      aho({"patterns": ["a"], "texts": []}),
      {"counts": []})

check("aho duplicates",
      aho({"patterns": ["he", "she", "he"],
           "texts": ["sheshe", ""]}),
      {"counts": [[2, 2, 2], [0, 0, 0]]})

check("aho overlap",
      aho({"patterns": ["a", "aa"],
           "texts": ["aaa"]}),
      {"counts": [[3, 2]]})


# 7. STRESS TESTS
long_text = "a" * 3000
long_pattern = "a" * 99 + "b"

for name, algorithm in [
    ("naive", naive), ("kmp", kmp), ("rk", rk)
]:
    check(
        f"{name} stress",
        algorithm({
            "text": long_text,
            "pattern": long_pattern
        })["positions"],
        []
    )

check("suffix stress",
      suffix({"text": "a" * 3000})["repeated"],
      "a" * 2999)

check("aho stress",
      aho({"patterns": ["a", "aa"],
           "texts": ["a" * 3000]})["counts"],
      [[3000, 2999]])


print(f"\nAll {passed} own tests passed!")
