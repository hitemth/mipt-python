import sys
import argparse
cardinality = 26
most_often = 4


def read(input_file):
    """
    returns string from file
    Args: input_file(file)
    Returns:text(str)
    """
    with open(input_file) as fin:
            text = fin.read()
    return text


def write(text, output_file):
    """
     writes string into file
     Args: output_file(file)
     Returns: none
     """
    with open(output_file, "w") as fout:
        fout.write(text)


def number(l):
    """
    returns letter number in the alphabet(no difference capital letter or not).Returns -1 if l is not letter.
    Args: l(char)
    Returns: int
    """
    if l.isalpha():
        if l >= 'a':
            return ord(l) - ord('a')
        else:
            return ord(l) - ord('A')
    else:
        return -1   # если входящий символ не буква, то в список-счетчик этот символ не попадет


def shift(l, key):
    """
    Makes letter shift right on 'key' steps. Returns new letter.
    Args: l(char),key(int)
    Returns: l(char)
    """
    if l.isalpha():
        if l >= 'a':
            return chr((number(l) + key) % cardinality + ord('a'))
        else:
            return chr((number(l) + key) % cardinality + ord('A'))
    else:
        return l


def encoding(cipher, key, text):
    """
    Returns string after encoding text with caesar/vigenere/vernam ciphers
    Args: cipher(str), key(str), text(str)
    Returns: str
    """
    s = str(text)
    if cipher == 'caesar':
        return ''.join(map(lambda c: shift(c, int(key)), s))
    if cipher == 'vigenere':
        return ''.join(map(lambda i: shift(s[i], number(key[i % len(key)])), range(len(s))))
    if cipher == 'vernam':
        text = list(text)
        for i in range(len(text)):
            text[i] = chr((ord(text[i]) + ord(key[i]) - 2 * (ord('a'))) % cardinality + ord('a'))
        return ''.join(text)
    else:
        print('cipher must be: caesar or vigenere or vernam')


def encode(cipher, key, input_file, output_file):
    """
    Write encrypted text in file
    Args: cipher(str), key(str), input_file(file), output_file(file)
    Returns: none
    """
    s = read(input_file)
    s1 = encoding(cipher, key, s)
    write(s1, output_file)


def decode(cipher, key, input_file, output_file):
    """
    Write decrypted text in file
    Args: cipher(str), key(str), input_file(file), output_file(file)
    Returns: none
    """
    if cipher == 'caesar':
        encode(cipher, cardinality - int(key), input_file, output_file)
    elif cipher == 'vigenere':
        key.lower()
        key = ''.join(map(lambda c: chr((cardinality - number(c)) % cardinality + ord('a')), key))
        encode(cipher, key, input_file, output_file)
    elif cipher == 'vernam':
        text = list(read(input_file))
        for i in range(len(text)):
            text[i] = chr((ord(text[i]) - ord(key[i])) % cardinality + ord('a'))
        s1 = ''.join(text)
        write(s1, output_file)

    else:
        print('cipher must be: caesar or vigenere or vernam')


def hack(input_file, output_file):
    """
    Caesar’s cipher cracker. Counts key-shift as
    difference between most frequent letter number in input_file and "e" number in alphabet. Write encoded text
    in output_file
    Args: input_file(file), output_file(file)
    Returns: none
    """
    text = list(read(input_file))
    counter_ = [0]*cardinality
    for l in text:
        if l.isalpha():
            counter_[number(l)] += 1
    m = counter_.index(max(counter_))
    key = most_often - m
    for i in range(len(text)):
        text[i] = shift(text[i], key)
    t = ''.join(text)
    write(t, output_file)


def create_parser():
    """
    Makes it convenient to work through the console
    Args: encode(str), decode(str), hack(str), cipher(str), key(str), input_file(file), output_file(file)
    Returns: parser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    encode_parser = subparsers.add_parser('encode')
    encode_parser.add_argument('--cipher', required=True)
    encode_parser.add_argument('--key', required=True)
    encode_parser.add_argument('--input-file')
    encode_parser.add_argument('--output-file')
    decode_parser = subparsers.add_parser('decode')
    decode_parser.add_argument('--cipher', required=True)
    decode_parser.add_argument('--key', required=True)
    decode_parser.add_argument('--input-file')
    decode_parser.add_argument('--output-file')
    hack_parser = subparsers.add_parser('hack')
    hack_parser.add_argument('--input-file')
    hack_parser.add_argument('--output-file')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.command == 'encode':
        encode(namespace.cipher, namespace.key, namespace.input_file, namespace.output_file)
    elif namespace.command == 'decode':
        decode(namespace.cipher, namespace.key, namespace.input_file, namespace.output_file)
    elif namespace.command == 'hack':
        hack(namespace.input_file, namespace.output_file)
    else:
        print('ERROR: No such command')
