def encrypt(target, number):
    alphabet = list("abcçdefgğhıijklmnoöpqrsştuüvwxyz")
    alphabetBig = list("ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZ")
    targetlist = list(target)
    resultlist = []
    for i in targetlist:
        if i in alphabetBig:
            index = alphabetBig.index(i) + number
            if index > len(alphabetBig) - 1:
                index = index % (len(alphabetBig) - 1) - 1
            resultlist.append(alphabetBig[index])
            del index
        elif i in alphabet:
            index = alphabet.index(i) + number
            if index > len(alphabet) - 1:
                index = index % (len(alphabet) - 1) - 1
            resultlist.append(alphabet[index])
            del index
        else:
            resultlist.append(i)
    result = ""
    for i in resultlist:
        result += i
    return result