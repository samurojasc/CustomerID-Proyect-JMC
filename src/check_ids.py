def check_sequences(id_str):
    digits = [int(d) for d in id_str]
    is_ascending = all(d1 < d2 for d1, d2 in zip(digits, digits[1:]))
    is_descending = all(d1 > d2 for d1, d2 in zip(digits, digits[1:]))
    return int(is_ascending), int(is_descending)


def check_repetitive_patterns(id_str):
    return int(id_str == id_str[:2] * (len(id_str) // 2))


def check_ids(id_str):
    ascend, descend = check_sequences(id_str)
    return len(id_str), len(set(id_str)) < len(id_str), ascend, descend, check_repetitive_patterns(id_str)
