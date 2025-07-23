import CreateSubkey as cs
import f_func as f

def Hex2bin(text):
    result = []
    for i in range(len(text)):
        result.extend(f.int2bit(int(text[i], 16)))
    return result

def bin2Hex(text):
    result = []
    q = len(text) // 4
    for i in range(q):
        dec = int(text[4 * i]) * 8 + int(text[4 * i + 1]) * 4 + int(text[4 * i + 2]) * 2 + int(text[4 * i + 3]) * 1
        x = hex(dec)[2:].upper()
        result.extend(x)
    rs = ''.join(result)
    return rs

def Encryption(text, key):
    keylist = cs.Subkey(keybit)
    text1 = f.IP(text, 0)
    L = [text1[i] for i in range(32)]
    R = [text1[i] for i in range(32, 64)]
    for i in range(16):
        tmp = R
        tmp = f.Extend(tmp)
        tmp = f.Xor(tmp, keylist[i])
        tmp = f.S_replace(tmp)
        tmp = f.P_replace(tmp)
        tmp = f.Xor(tmp, L)
        L = R
        R = tmp
    L, R = R, L
    ctext = L
    ctext.extend(R)
    ctext = f.IP(ctext, 1)
    return bin2Hex(ctext)

def Decryption(text, key):
    keylist = cs.Subkey(keybit)
    text1 = f.IP(text, 0)
    L = [text1[i] for i in range(32)]
    R = [text1[i] for i in range(32, 64)]
    for i in range(16):
        tmp = R
        tmp = f.Extend(tmp)
        tmp = f.Xor(tmp, keylist[15 - i])
        tmp = f.S_replace(tmp)
        tmp = f.P_replace(tmp)
        tmp = f.Xor(tmp, L)
        L = R
        R = tmp
    L, R = R, L
    ctext = L
    ctext.extend(R)
    ctext = f.IP(ctext, 1)
    return bin2Hex(ctext)

if __name__ == '__main__':
    plaintext = input('Введите сообщение (8 символов ENG / 4 - RUS): ')
    PT_hex = plaintext.encode('utf-8').hex()
    print('Сообщение в HEX: ' + PT_hex)
    key = input('Введите ключ (8 символов ENG / 4 - RUS): ')
    KEY_hex = key.encode('utf-8').hex()
    ptext = Hex2bin(PT_hex)
    keybit = Hex2bin(KEY_hex)
    t = Encryption(ptext, keybit)
    t2 = Hex2bin(t)
    print('Закодировано: ' + t)
    print('Раскодировано: ' + Decryption(t2, keybit))
