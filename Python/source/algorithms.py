"""Implement algorithm bodies. See docs/guide/CONTRACTS.md; inputs and outputs are dictionaries."""

def lcs(request):
    a = request["a"]
    b = request["b"]
    n = len(a)
    m = len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i = n
    j = m
    sequence = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            sequence.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    sequence.reverse()
    return {
        "length": dp[n][m],
        "sequence": "".join(sequence)
    }


def merge(request):
    sizes = request["sizes"]
    n = len(sizes)
    if n <= 1:
        return {"cost": 0, "plan": []}
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + sizes[i]
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            total = prefix[r + 1] - prefix[l]
            best = float("inf")
            for k in range(l, r):
                cost = dp[l][k] + dp[k + 1][r] + total
                if cost < best:
                    best = cost
                    split[l][r] = k
            dp[l][r] = best
    plan = []
    def build(l, r):
        if l == r:
            return
        k = split[l][r]
        build(l, k)
        build(k + 1, r)
        plan.append([l, k, r])
    build(0, n - 1)
    return {
        "cost": dp[0][n - 1],
        "plan": plan
    }



def tree(request):
    n = request["n"]
    weights = request["weights"]
    edges = request["edges"]
    if n == 0:
        return {"weight": 0, "selected": []}
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    parent = [-1] * n
    parent[0] = 0
    order = [0]
    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)
    take = [0] * n
    skip = [0] * n
    for u in reversed(order):
        take[u] = weights[u]
        skip[u] = 0
        for v in graph[u]:
            if parent[v] == u:
                take[u] += skip[v]
                skip[u] += max(take[v], skip[v])
    selected = []
    stack = [(0, False)]
    while stack:
        u, parent_taken = stack.pop()
        choose = (
            not parent_taken
            and take[u] > skip[u]
        )
        if choose:
            selected.append(u)
        for v in graph[u]:
            if parent[v] == u:
                stack.append((v, choose))
    return {
        "weight": max(take[0], skip[0]),
        "selected": selected
    }


def naive(request):
    text = request["text"]
    pattern = request["pattern"]
    n = len(text)
    m = len(pattern)
    if m == 0:
        return {"positions": list(range(n + 1))}
    if m > n:
        return {"positions": []}
    positions = []
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)
    return {"positions": positions}


def kmp(request):
    text = request["text"]
    pattern = request["pattern"]
    n = len(text)
    m = len(pattern)
    if m == 0:
        return {"positions": list(range(n + 1))}
    if m > n:
        return {"positions": []}
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    positions = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            positions.append(i - m + 1)
            j = pi[j - 1]
    return {"positions": positions}


def rk(request):
    text = request["text"]
    pattern = request["pattern"]
    n = len(text)
    m = len(pattern)
    if m == 0:
        return {"positions": list(range(n + 1))}
    if m > n:
        return {"positions": []}
    base = 31
    mod = 101
    pattern_hash = 0
    window_hash = 0
    highest_power = pow(base, m - 1, mod)
    for i in range(m):
        pattern_hash = (
            pattern_hash * base + ord(pattern[i])
        ) % mod
        window_hash = (
            window_hash * base + ord(text[i])
        ) % mod
    positions = []
    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(i)
        if i < n - m:
            window_hash = (
                (window_hash - ord(text[i]) * highest_power)
                * base
                + ord(text[i + m])
            ) % mod
    return {"positions": positions}


def suffix(request):
    text = request["text"]
    n = len(text)
    if n == 0:
        return {
            "sa": [],
            "lcp": [],
            "repeated": ""
        }
    sa = list(range(n))
    rank = [ord(c) for c in text]
    k = 1
    while True:
        sa.sort(
            key=lambda i: (
                rank[i],
                rank[i + k] if i + k < n else -1
            )
        )
        new_rank = [0] * n
        for i in range(1, n):
            prev = sa[i - 1]
            curr = sa[i]
            prev_pair = (
                rank[prev],
                rank[prev + k] if prev + k < n else -1
            )
            curr_pair = (
                rank[curr],
                rank[curr + k] if curr + k < n else -1
            )
            new_rank[curr] = new_rank[prev] + (
                1 if prev_pair != curr_pair else 0
            )
        rank = new_rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    lcp = [0] * n
    inv = [0] * n
    for i in range(n):
        inv[sa[i]] = i
    h = 0
    for i in range(n):
        pos = inv[i]
        if pos == 0:
            h = 0
            continue
        j = sa[pos - 1]
        while (
            i + h < n
            and j + h < n
            and text[i + h] == text[j + h]
        ):
            h += 1
        lcp[pos] = h
        if h > 0:
            h -= 1
    best_length = 0
    best_start = 0
    for i in range(1, n):
        if lcp[i] > best_length:
            best_length = lcp[i]
            best_start = sa[i]
    repeated = text[best_start:best_start + best_length]
    return {
        "sa": sa,
        "lcp": lcp,
        "repeated": repeated
    }


def aho(request):
    from collections import deque
    patterns = request["patterns"]
    texts = request["texts"]
    p = len(patterns)
    if p == 0:
        return {"counts": [[] for _ in texts]}
    if not texts:
        return {"counts": []}
    children = [{}]
    fail = [0]
    terminals = []
    for pattern in patterns:
        state = 0
        for char in pattern:
            if char not in children[state]:
                children[state][char] = len(children)
                children.append({})
                fail.append(0)
            state = children[state][char]
        terminals.append(state)
    queue = deque()
    order = [0]
    for child in children[0].values():
        queue.append(child)
        order.append(child)
    while queue:
        state = queue.popleft()
        for char, nxt in children[state].items():
            f = fail[state]
            while f != 0 and char not in children[f]:
                f = fail[f]
            fail[nxt] = children[f].get(char, 0)
            queue.append(nxt)
            order.append(nxt)
    counts = []
    states_count = len(children)
    for text in texts:
        visits = [0] * states_count
        state = 0
        for char in text:
            while state != 0 and char not in children[state]:
                state = fail[state]
            state = children[state].get(char, 0)
            visits[state] += 1
        for state in reversed(order[1:]):
            visits[fail[state]] += visits[state]
        row = [visits[state] for state in terminals]
        counts.append(row)
    return {"counts": counts}