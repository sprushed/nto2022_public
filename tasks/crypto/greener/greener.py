flag = b"NTO{c0d1n6_7h30ry_15_v3ry_1n73r3571n6}"


def green_code(message: bytes):
    arr = [0] + list(message)
    new_arr = []
    for i in range(1, len(arr)):
        new_arr.append(arr[i - 1] ^ arr[i])
    return bytes(new_arr)


code = green_code(flag)
print(f"code = {code}")
