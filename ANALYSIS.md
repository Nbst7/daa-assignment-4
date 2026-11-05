# Assignment 4 — analysis (complete in English)

## Environment and commands

**Programming language:** Python 3.12.10

**Operating system:** Microsoft Windows 11 Pro

**Processor:** AMD Ryzen 7 7735HS with Radeon Graphics

**RAM:** 16 GB (approximately 15.19 GiB)

**Development environment:** Windows PowerShell

**Setup command:**
```powershell
python tools/run.py --setup
```

**Testing command:**
```powershell
python tools/run.py --check
```

**Testing results:**
- All 44 public tests passed.
- State reset test passed.
- All eight required algorithms were implemented in Python.

**Submission:** The final commit URL will be submitted to Moodle after completing the project.

## Algorithm explanations

### 1. LCS (Longest Common Subsequence)

**State:** `dp[i][j]` stores the length of the longest common subsequence of the first `i` characters of string `a` and the first `j` characters of string `b`.

**Base cases:** `dp[i][0] = 0` and `dp[0][j] = 0`, because an empty string has no common subsequence with another string.

**Transition:** If `a[i-1] == b[j-1]`, we use `dp[i-1][j-1] + 1`. Otherwise, we take the maximum of `dp[i-1][j]` and `dp[i][j-1]`.

**Processing order:** The table is filled from top to bottom and left to right. All required previous values are already calculated.

**Correctness:** Every common subsequence either uses the matching last characters or skips a character from one of the strings. The DP considers these possibilities and chooses the best one.

**Reconstruction:** We move backwards from `dp[n][m]`. Matching characters are added to the answer. When two choices have equal values, the implementation moves upward. The resulting sequence is reversed at the end.

**Complexity:** Time O(n × m), memory O(n × m), plus the returned sequence of at most min(n, m) characters. Python lists are used for the DP table.

**Boundary test:** An empty input string must return length 0 and an empty sequence.

### 2. Merge (Optimal Adjacent Merge)

**State:** `dp[l][r]` stores the minimum cost of merging all elements from index `l` to index `r`.

**Base case:** One element requires no merge, so `dp[i][i] = 0`. Empty and single-element inputs return cost 0 and an empty plan.

**Transition:** For every possible split `k`, calculate `dp[l][k] + dp[k+1][r] + total`, where `total` is the sum of the elements in the interval.

**Processing order:** Intervals are processed from shorter to longer. Smaller intervals are already solved when they are needed.

**Correctness:** The last merge of an interval must combine two adjacent groups. Trying every possible split and choosing the minimum gives the optimal cost.

**Reconstruction:** The `split` table stores the best split position. A recursive function builds the left plan, then the right plan, and finally adds the current merge. Equal costs keep the first split found.

**Complexity:** Time O(n³), memory O(n²), including the DP and split tables. Prefix sums allow O(1) interval sum queries. The output plan contains n − 1 merges for n greater than zero.

**Boundary test:** A single element must return cost 0 with no merge operations.

### 3. Tree (Maximum Weight Independent Set)

**State:** `take[u]` stores the best weight in the subtree rooted at node `u` when node `u` is selected. `skip[u]` stores the best weight when node `u` is not selected.

**Base case:** For a leaf, `take[u] = weights[u]` and `skip[u] = 0`.

**Transition:** If node `u` is selected, its children cannot be selected. If it is skipped, each child can be selected or skipped.

**Processing order:** The tree is traversed from root 0 to create a parent array and an order list. DP values are then calculated in reverse order, so children are processed before parents.

**Correctness:** Every valid independent set either contains a node or does not contain it. The two DP states consider both possibilities and combine optimal child solutions.

**Reconstruction:** An iterative stack reconstructs the selected nodes. A node is selected only if its parent was not selected and `take[u] > skip[u]`. Ties are resolved by skipping the node.

**Complexity:** Time O(n), memory O(n), including adjacency lists, parent information, DP arrays, traversal data, and the selected-node output.

**Boundary test:** A tree with negative weights should allow selecting no nodes, with total weight 0.

### 4. Naive String Matching

**State:** Index `i` represents the starting position in the text. Index `j` represents the character being compared inside the pattern.

**Base cases:** An empty pattern matches at all n + 1 boundaries. A pattern longer than the text has no matches.

**Update:** For every possible starting position, compare the pattern characters with the corresponding text characters. Stop early if a mismatch is found.

**Processing order:** Starting positions are checked from left to right, so output positions are sorted.

**Correctness:** Every possible starting position is examined. A position is added only when all pattern characters match.

**Complexity:** Worst-case time O(n × m), auxiliary memory O(1), excluding the output list. The output can contain up to n + 1 positions.

**Boundary test:** Searching for `"aa"` in `"aaaa"` must return `[0, 1, 2]`, including overlapping matches.

### 5. KMP (Knuth–Morris–Pratt)

**State:** `pi[i]` stores the length of the longest proper prefix of the pattern that is also a suffix of the pattern ending at index `i`. During searching, `j` stores the number of currently matched pattern characters.

**Base cases:** An empty pattern matches at all boundaries. A pattern longer than the text returns no matches. The first prefix value is zero.

**Update:** The prefix array is built using previous prefix values. During searching, mismatches use `pi[j-1]` to find the next possible prefix without restarting the comparison.

**Processing order:** The prefix array is built from left to right before searching the text from left to right.

**Correctness:** The prefix array records the longest reusable matching prefix. After a mismatch, shorter impossible prefixes can be skipped without losing any valid match.

**Reconstruction:** When `j == m`, the starting position `i-m+1` is added. The algorithm then uses the prefix array to continue searching, including overlapping matches.

**Complexity:** Time O(n + m), auxiliary memory O(m), excluding output positions.

**Boundary test:** Searching for `"aaa"` in `"aaaaa"` must return `[0, 1, 2]`.

### 6. Rabin–Karp

**State:** `pattern_hash` stores the pattern hash, and `window_hash` stores the hash of the current text window.

**Base cases:** An empty pattern matches at all boundaries. If the pattern is longer than the text, the answer is empty.

**Update:** The implementation uses polynomial rolling hashing with base 31, modulus 101, and `ord()` character codes. The highest power is used to remove the leftmost character before adding the next character.

**Processing order:** The initial hashes are calculated first. Then text windows are processed from left to right.

**Correctness:** Equal strings have equal hashes, but different strings can also have equal hashes. Therefore, the implementation checks the actual characters whenever the hashes match. This prevents false matches caused by collisions.

**Complexity:** Time O(n + m + c × m), where `c` is the number of windows with a hash equal to the pattern hash. Worst-case time is O(n × m + n + m). Auxiliary memory is O(1), excluding output positions.

**Boundary test:** Searching for `"ab"` in `"abdj"` must return `[0]`. The strings `"ab"` and `"dj"` have the same hash under base 31 and modulus 101, so this checks collision verification.

### 7. Suffix Array and Kasai LCP

**Suffix array state:** `sa` contains the starting positions of nonempty suffixes in lexicographic order. `rank[i]` represents the current rank of the suffix starting at position `i`.

**Suffix array update:** Prefix doubling sorts suffixes using pairs of ranks for the first `k` and next `k` characters. After each sorting step, new ranks are assigned and `k` is doubled.

**Suffix array base case:** An empty string returns empty arrays and an empty repeated substring. For a nonempty string, initial ranks are character codes.

**Processing order:** Every iteration uses ranks calculated in the previous iteration. The process stops when all suffixes have different ranks.

**Correctness:** At each iteration, the rank pairs correctly order prefixes of increasing length. When every suffix has a unique rank, the complete suffix order is determined.

**Kasai state:** `inv[i]` gives the position of suffix `i` in the suffix array. `h` stores the reusable common-prefix length.

**Kasai update:** For every suffix, the algorithm compares it with the previous suffix in sorted order. After each comparison, the common-prefix length can decrease by at most one for the next original-text position.

**Kasai correctness:** The algorithm calculates the exact common-prefix length of each adjacent pair of sorted suffixes. Reusing `h` avoids repeating unnecessary comparisons.

**Longest repeated substring:** The maximum LCP value gives the length of a longest repeated substring. The implementation returns the corresponding substring. Overlapping repetitions are allowed. Equal maximum lengths keep the first one found.

**Complexity:** Prefix doubling takes O(n log² n) time using Python's built-in list sorting with rank-pair keys. Kasai takes O(n) time. Total auxiliary memory is O(n), excluding the returned suffix array, LCP array, and repeated substring.

**Boundary test:** For `"banana"`, the suffix array is `[5, 3, 1, 0, 4, 2]`, LCP is `[0, 1, 3, 0, 0, 2]`, and the longest repeated substring is `"ana"`.

### 8. Aho–Corasick

**State:** A trie stores all patterns. `children` stores transitions between states, `fail` stores failure links, and `terminals` stores the final state of each pattern in input order.

**Base cases:** An empty pattern dictionary returns an empty count list for every text. An empty list of texts returns an empty result.

**Construction:** Every pattern is inserted into the trie. Failure links are calculated using breadth-first search with a deque.

**Processing order:** Trie construction happens first. Failure links are built in BFS order, so the failure information needed for a state is already available.

**Search update:** Each text is scanned from left to right. On a missing transition, the algorithm follows failure links until a valid transition is found or the root is reached.

**Counting:** Each visited state gets a count. Counts are propagated in reverse BFS order through failure links. This includes patterns that are suffixes of longer matched patterns.

**Correctness:** Trie transitions recognize matching prefixes, and failure links preserve possible suffix matches. Reverse propagation adds every matching occurrence to its terminal state. Duplicate patterns share a terminal state but receive separate output entries.

**Reset:** The search state and visit counters are recreated for every text. All data structures are local to the function, so independent requests do not share state.

**Complexity:** Let L be the total pattern length, T the total length of all texts, S the number of trie states, P the number of patterns, and Q the number of texts. Trie construction takes O(L). The BFS and failure-link searches take O(L × D) in the worst case, where D is the maximum failure-chain length, because transitions are stored in Python dictionaries and missing transitions may follow failure links. Searching takes O(T + Q × S + Q × P) with amortized failure transitions and per-text count propagation. Auxiliary memory is O(L + S + P), excluding the output matrix of size O(Q × P).

**Boundary test:** Patterns `["he", "she", "he"]` with text `"sheshe"` must return `[2, 2, 2]`. This checks suffix matches, duplicates, and multiple occurrences.

## Own tests

I created `own_tests.py` to test Naive, KMP, and Rabin–Karp with the same inputs. Every algorithm was checked against expected positions using Python assertions.

**Command:** `tests/student/own_tests.py`

| Command | Input or fixture path | Expected result | Actual result / log | What it checks |
|---|---|---|---|---|
| `python tests/student/own_tests.py` | `tests/student/own_tests.py`: `"aaaaa"`, `"aaa"` | `[0, 1, 2]` | PASS for all 3 algorithms | Overlapping matches |
| `python tests/student/own_tests.py` | `tests/student/own_tests.py`: `"abc"`, `""` | `[0, 1, 2, 3]` | PASS for all 3 algorithms | Empty pattern |
| `python tests/student/own_tests.py` | `tests/student/own_tests.py`: `"ab"`, `"abcd"` | `[]` | PASS for all 3 algorithms | Pattern longer than text |
| `python tests/student/own_tests.py` | `tests/student/own_tests.py`: `"abdj"`, `"ab"` | `[0]` | PASS for all 3 algorithms | Rabin–Karp hash collision |
| `python tests/student/own_tests.py` | `tests/student/own_tests.py`: `"aAaA"`, `"Aa"` | `[1]` | PASS for all 3 algorithms | Case-sensitive matching |

I also ran `python tools/run.py --check`. All 44 public tests and the state reset test passed.

### Extended student tests

I created `tests/student/own_tests.py` to test all eight implemented algorithms.

**Command:** `python tests/student/own_tests.py`

**Actual result:** All 44 own tests passed.

The tests cover:
- LCS: empty inputs, repeated characters, and subsequences.
- Merge: empty inputs, single blocks, two blocks, and zero sizes.
- Tree: empty trees, negative weights, and a small chain.
- Naive, KMP, and Rabin–Karp: overlaps, empty patterns, long patterns, hash collisions, case sensitivity, and punctuation.
- Suffix Array: empty strings, single characters, `"banana"`, and repeated characters.
- Aho–Corasick: empty dictionaries, no texts, duplicate patterns, suffix matches, and overlapping matches.
- Stress tests: long repetitive strings for string matching, suffix arrays, and Aho–Corasick.

All expected outputs were checked using Python assertions. The results were produced by running the tests locally.

The public test suite was also executed with `python tools/run.py --check`, and all 44 public cases and the state reset check passed.

## Search comparison

I compared Naive, KMP, and Rabin–Karp using the same input strings for each algorithm.

**Environment:** Python 3.12.10, Windows 11 Pro, AMD Ryzen 7 7735HS, 16 GB RAM.

**Benchmark command:** `python benchmark.py`

**Results file:** `benchmark_results.csv`

**Generator:** Python `random.Random(42)` with alphabet `abcd` for random strings. Repetitive texts contain only `a`, while patterns contain `m-1` characters `a` followed by `b`.

**Input sizes:** (300, 10), (1000, 30), and (3000, 100), where n is text length and m is pattern length.

**Correctness verification:** Before timing, all algorithms were checked against Naive results using assertions. Every timed result was also checked.

**Timing method:** `time.perf_counter()` was used to measure only the algorithm function call. Each algorithm received one unmeasured warm-up call followed by three measured runs. The median was calculated using `statistics.median()`. Python startup and compilation were excluded. No JIT compilation was used.

**Time unit:** milliseconds (ms).

### Benchmark summary

| Case | n | m | Naive median (ms) | KMP median (ms) | RK median (ms) |
|---|---:|---:|---:|---:|---:|
| Random | 300 | 10 | 0.1133 | 0.0347 | 0.1010 |
| Random | 1000 | 30 | 0.1538 | 0.1551 | 0.3309 |
| Random | 3000 | 100 | 0.8840 | 0.2711 | 0.9540 |
| Repetitive | 300 | 10 | 0.2265 | 0.0610 | 0.1371 |
| Repetitive | 1000 | 30 | 2.3458 | 0.1814 | 0.3165 |
| Repetitive | 3000 | 100 | 22.3200 | 0.8307 | 1.0319 |

The complete table containing all three raw measurements, seeds, input sizes, medians, and correctness checks is saved in `benchmark_results.csv`.

### Full benchmark results

All times are measured in milliseconds (ms). The random generator uses seed 42. Each algorithm was tested three times after one warm-up run. All returned positions were checked for correctness.

| Case | n | m | Seed/generator | Algorithm | Run 1 | Run 2 | Run 3 | Median | Correct outputs checked |
|---|---:|---:|---|---|---:|---:|---:|---:|---|
| Random | 300 | 10 | 42 / abcd | Naive | 0.1143 | 0.1133 | 0.1110 | 0.1133 | YES |
| Random | 300 | 10 | 42 / abcd | KMP | 0.0347 | 0.0277 | 0.0425 | 0.0347 | YES |
| Random | 300 | 10 | 42 / abcd | RK | 0.1010 | 0.1356 | 0.0978 | 0.1010 | YES |
| Random | 1000 | 30 | 42 / abcd | Naive | 0.1588 | 0.1518 | 0.1538 | 0.1538 | YES |
| Random | 1000 | 30 | 42 / abcd | KMP | 0.1647 | 0.1551 | 0.0935 | 0.1551 | YES |
| Random | 1000 | 30 | 42 / abcd | RK | 0.3318 | 0.3309 | 0.3267 | 0.3309 | YES |
| Random | 3000 | 100 | 42 / abcd | Naive | 0.8840 | 0.8981 | 0.7519 | 0.8840 | YES |
| Random | 3000 | 100 | 42 / abcd | KMP | 0.2668 | 0.3081 | 0.2711 | 0.2711 | YES |
| Random | 3000 | 100 | 42 / abcd | RK | 0.9540 | 1.0335 | 0.5619 | 0.9540 | YES |
| Repetitive | 300 | 10 | a × n, a × (m−1) + b | Naive | 0.2265 | 0.2382 | 0.1897 | 0.2265 | YES |
| Repetitive | 300 | 10 | a × n, a × (m−1) + b | KMP | 0.0728 | 0.0610 | 0.0526 | 0.0610 | YES |
| Repetitive | 300 | 10 | a × n, a × (m−1) + b | RK | 0.1201 | 0.1371 | 0.2140 | 0.1371 | YES |
| Repetitive | 1000 | 30 | a × n, a × (m−1) + b | Naive | 2.3458 | 3.5337 | 1.9679 | 2.3458 | YES |
| Repetitive | 1000 | 30 | a × n, a × (m−1) + b | KMP | 0.2230 | 0.1721 | 0.1814 | 0.1814 | YES |
| Repetitive | 1000 | 30 | a × n, a × (m−1) + b | RK | 0.3165 | 0.3137 | 0.3198 | 0.3165 | YES |
| Repetitive | 3000 | 100 | a × n, a × (m−1) + b | Naive | 22.3200 | 20.8940 | 24.0266 | 22.3200 | YES |
| Repetitive | 3000 | 100 | a × n, a × (m−1) + b | KMP | 0.8307 | 0.9014 | 0.5606 | 0.8307 | YES |
| Repetitive | 3000 | 100 | a × n, a × (m−1) + b | RK | 1.0117 | 1.0319 | 1.1940 | 1.0319 | YES |

The complete benchmark results are also saved in `benchmark_results.csv`.

### Observations

KMP performed well on both random and repetitive inputs. Its prefix function helps avoid repeated character comparisons.

Naive performed reasonably on random inputs because mismatches often happened early. However, on repetitive inputs, it became much slower because many characters matched before the final mismatch.

Rabin–Karp used rolling hashes with base 31 and modulus 101. It performed better than Naive on the largest repetitive input but was slower than KMP in these measurements.

The small modulus increases the possibility of hash collisions. When hashes match, the implementation verifies actual characters, which can increase execution time. This result applies to this implementation and should not be generalized to all Rabin–Karp implementations.

The collision test with text `"abdj"` and pattern `"ab"` returned `[0]`, confirming that the algorithm does not accept false matches caused by equal hashes.

These measurements describe the observed performance on this computer. They do not prove the theoretical time complexity of the algorithms.

## Sources and AI assistance

### Sources and Tools

- Assignment 4 instructions and `docs/guide/CONTRACTS.md` were used to understand the required algorithms, input/output formats, constraints, and testing requirements.
- Python 3.12.10 was used to implement and run the algorithms.
- Windows PowerShell was used to execute commands and tests.
- Git and GitHub were used for version control and submission.
- ChatGPT (OpenAI) was used only for troubleshooting and understanding error messages encountered during development.

### AI Contribution

ChatGPT was used to help identify possible causes of coding errors and explain debugging issues. All algorithm implementations, testing, benchmarking, and final code integration were completed by me.

### My Verification

I ran `tests/student/own_tests.py`, which completed 44 checks successfully. I also ran `benchmark.py`, which generated 54 timing measurements in `benchmark_results.csv`.