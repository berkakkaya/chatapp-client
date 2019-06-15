from math import sqrt
from random import choice,randrange
a=[]

def SavePrimes():
    for i in range(1,500):
        IsPrime=True
        end=int(sqrt(i))+1
        for j in range(2,end):
            if i%j==0:
                IsPrime=False
                break
        if IsPrime==True:a.append(i)

def ChoicePQAndCountUpTotient():
    global p,q,n,tn
    p,q=choice(a),choice(a)
    n=p*q
    tn=(p-1)*(q-1)

def ChoiceE():
    global e
    while True:
        e=choice(a)
        if e<tn and IsRelativelyPrimeNumbers(e)==True:break

def IsRelativelyPrimeNumbers(etmp):#Fermat teoremi
        if pow(tn,(etmp-1))%etmp==1:return True
        else:return False

def xgcd(a, b):#Extended Euclid
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def FindD(a, b):
    global d
    g, x, _ = xgcd(a, b)
    if g == 1:
        d= x % b
    
def CleanTextASCII(text):
    CleanText=""
    for i in text:
        AsciiText=str(ord(i))
        if len(AsciiText)<3:CleanText+=(3-len(AsciiText))*"0"+AsciiText
        else:CleanText+=AsciiText
    return CleanText

def CipherTemp(temp):
    CipTemp=str((int(temp)**e)%n)
    t=len(str(n))-len(CipTemp)
    if t!=0:  return (str("0"*t+CipTemp))
    return CipTemp
    
def GetCipherText(text):
    CleanText=CleanTextASCII(text)
    global CipherText
    CipherText=""
    BasamakSayisi=len(str(n))-1
    for i in range(0,len(CleanText),BasamakSayisi):
        tmp=CleanText[i:(i+BasamakSayisi)]
        if len(tmp)!=BasamakSayisi:tmp+=(BasamakSayisi-len(tmp))*"0"
        CipherText+=CipherTemp(tmp)

def Sifrele(getmessage):
    SavePrimes()
    ChoicePQAndCountUpTotient()
    ChoiceE()
    FindD(e,tn)
    GetCipherText(getmessage)
    return CipherText,n,e,d
    
def SifreCoz(GetCipherText,nn,ee,dd):
    ClearText=""
    NLenght=len(str(nn))
    for i in range(0,len(GetCipherText),NLenght):
        tmp=GetCipherText[i:(i+NLenght)]
        tmp=(int(tmp)**dd)%nn
        if len(str(tmp))!=(NLenght):
            tmp=(NLenght-len(str(tmp))-1)*"0"+str(tmp)
        ClearText=ClearText+str(tmp)
    return ASCIItoString(ClearText)
  
def ASCIItoString(Text):
    TextClear=""    
    for i in range(0,len(Text),3):
        TextClear+=chr(int(Text[i:i+3]))
    return TextClear









