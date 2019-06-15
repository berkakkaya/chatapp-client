def decrypt(target, number):
    alphabet = list("abcçdefgğhıijklmnoöpqrsştuüvwxyz")
    alphabetBig = list("ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZ")
    targetlist = list(target)
    resultlist = []
    for i in targetlist:
        if i in alphabetBig:
            index = alphabetBig.index(i) - number
            resultlist.append(alphabetBig[index])
            del index
        elif i in alphabet:
            index = alphabet.index(i) - number
            resultlist.append(alphabet[index])
            del index
        else:
            resultlist.append(i)
    result = ""
    for i in resultlist:
        result += i
    return result