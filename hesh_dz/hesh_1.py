def rabinKarpAlgorithm(t, p):
    n = len(t)
    m = len(p)
    if m > n:
        return []

    list_i = []
    x = 263
    p_mod = 10**9 + 7

    def single_hash(ch, i):
        return (ord(ch) * pow(x, i, p_mod)) % p_mod

    def hash(s):
        h = 0
        for i, ch in enumerate(s):
            h = (h + single_hash(ch, i)) % p_mod
        return h


    p_hash = hash(p)


    h = hash(t[:m])


    x_m = pow(x, m - 1, p_mod)


    for i in range(n - m + 1):
        if p_hash == h:
            if t[i:i + m] == p:
                list_i.append(i)

        if i < n - m:

            h = (h - ord(t[i]) * x_m) % p_mod
            h = (h * x + ord(t[i + m])) % p_mod
            h = (h + p_mod) % p_mod

    return list_i

print(rabinKarpAlgorithm('abacaba', 'aba'))  # [0, 4]
print(rabinKarpAlgorithm('restTesttesT', 'Test'))  # [4]
print(rabinKarpAlgorithm('baaaaaaa', 'aaaaa'))  # [1, 2, 3] объясни код