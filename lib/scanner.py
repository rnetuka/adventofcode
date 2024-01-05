def tokenize(string, sep=None, types=()):
    parts = string.split(sep)
    r = min(len(parts), len(types))
    for i in range(r):
        parts[i] = types[i](parts[i])
    return parts
