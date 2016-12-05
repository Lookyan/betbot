
star = b'\xE2\xAD\x90'.decode()
digit_1 = b'\x31\xE2\x83\xA3'.decode()
digit_2 = b'\x32\xE2\x83\xA3'.decode()
digit_3 = b'\x33\xE2\x83\xA3'.decode()


def get_digit_smile(pos):
    if pos == 1:
        return '{}{}{}'.format(star, digit_1, star)
    elif pos == 2:
        return digit_2
    elif pos == 3:
        return digit_3
