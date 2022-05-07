# Arithmetic Coding

這個 repo 總共可分成三個部分：Arithmetic Coding、Adaptive Arithmetic Coding、Context-Modeling Adaptive Arithmetic Coding

## Introduction

Arithmetic coding 是將一段 text message 利用 0-1 的區間來表示。當 text message 越長，用來表示此 text message 的區間就越小，也就是代表 length of coding 就越長。

而越常出現的 text，區間縮小的速度就會越慢，則可以縮短 length of coding。隨著 length of text message 的增加，Arithmetic coding 之 entropy 可以趨近無雜訊編碼的理論極限。

另外，因為大部分的時候，無法事先統計好 probability distribution，因此又發明了另一種 algorithm - adaptive Arithmetic Coding。不需要事先給定 probability distribution，而是在對 text message 進行 encoding & decoding 的同時，去更新 probability distribution。

最後，為了對應到真實情況，使用了條件機率，也就是說不再只是單純地做 probability distribution，而是根據不同的 context condition 去做不同的機率統計，接著根據不同的 probability distribution 去做 encoding / decoding。

## Algorithm - Encoding

設定 data set 有 M 個可能的值（ex: 1, 2, .., M），每個 data 出現機率為 Pn，使用 k 進位進行編碼。

先計算 probability inteval of each element：

```python
s = 0
S = [s]
for p in P:
    s += p
    S.append(s)
```

接著，依序放入 text message，更新 lower & upper bound：

```python
for t in text:
    lower = lower + S[t-1] * (upper-lower)
    upper = lower + S[t] * (upper-lower)
```

為了避免當 length of text message 過長時，lower & upper bound 會極度接近，造成精度不足，出現 floating point error。
因此，當 lower bound > 0.5 或是 upper bound <= 0.5 時，會對於 lower bound 以及 upper bound 同時做擴增的動作。

```python
while lower > 0.5 or upper <= 0.5:
    if lower > 0.5:
        ciphertext += '1'
        lower = lower * 2 - 1
        upper = upper * 2 - 1
    elif upper <= 0.5:
        ciphertext += '0'
        lower *= 2
        upper *= 2
```

最後，得到 lower & upper bound 之後，通過計算找出 b & C，使得 lower bound < C * 2^(-b) < (C+1) * 2^(-b) < upper bound。

```python
while True:
    if 2**(-b) > (upper-lower):
        b += 1
    else:
        for C in range(2**(b)):
            if lower < C * 2**(-b) and (C+1) * 2**(-b) < upper:
                while_break = True
                break
        if while_break:
            break
        b += 1
```

找出 b & C 之後，encoding 的方式就是將 C 用 b 個 bits 的二進位去做表示。並且要記得加上前面在做擴增動作時，已經確定的 ciphertext。

```python
ciphertext = ciphertext + str(bin(C)[2:]).zfill(b)
```

## Algorithm - Decoding

設定 data set 有 M 個可能的值（ex: 1, 2, .., M），每個 data 出現機率為 Pn，使用 k 進位進行解碼，原始 length of data 為 N。

先計算 probability inteval of each element：

```python
s = 0
S = [s]
for p in P:
    s += p
    S.append(s)
```

接著依序放入 ciphtertext，並且透過 lower1 & upper1 bound 去計算原始 lower bound 跟 upper bound。

```python
lower, upper = 0, 1
lower1, upper1 = 0, 1
j = 0
for i in range(N):
    check = True
    while check:
        exist = False
        for n in range(len(S)):
            if lower + (upper-lower) * S[n] <= lower1 and lower + (upper-lower) * S[n+1] >= upper1:
                check = False
                exist = True
        if not exist:
            lower1 = lower1 + (ciphertext[j-1]+1) * 2**(-j)
            upper1 = lower1 + ciphertext[j-1] * 2**(-j)
    text += n
    lower = lower + (upper-lower) * S[n]
    upper = upper + (upper-lower) * S[n+1]
```

為了避免當 length of text message 過長時，lower & upper bound 會極度接近，造成精度不足，出現 floating point error。
因此，當 lower bound > 0.5 或是 upper bound <= 0.5 時，會對於 lower bound 以及 upper bound 同時做擴增的動作。
與 encoding 不同的地方在於，要同時對 lower & upper bound 以及 lower1 & upper1 bound 做擴增。

```python
while lower > 0.5 or upper <= 0.5:
    if lower > 0.5:
        lower = lower * 2 - 1
        upper = upper * 2 - 1
        lower1 = lower1 * 2 - 1
        upper1 = upper1 * 2 - 1
    elif upper <= 0.5:
        lower *= 2
        upper *= 2
        lower1 *= 2
        upper1 *= 2
```

## Adaptive Algorithm - Encoding

假設 data set 有 M 個值（ex: 1, 2, ..., M），因此 initial probability 設定為 uniform 的：

```python
dic = {'total':0}
for s in set:
    dic[s] = 1
    dic['total'] += 1
```

接著，encoding 的演算法與前面相同，只是每次 for loop 開始時，都要先重新計算過一次 inteval of probability，並且在 for loop 的最後要對 dic 去做更新。

```python
def inteval(dic):
    S = {}
    for k in dic.keys():
        if k != 'total':
            S[k] = [prev, prev + dic[k]/dic['total']]
            prev += dic[k]/dic['total']
    return S

for t in text:
    S = inteval(dic)
    lower = lower + S[t][0] * (upper-lower)
    upper = lower + S[t][1] * (upper-lower)
    dic[t] += 1
    dic['total'] += 1
```

接著同樣要去避免 floating point error，所以要做 lower & upper bound 的擴增動作。

最後，一樣找出 b & C 能夠符合 lower & upper bound condition。

找出 b & C 之後，encoding 的方式就是將 C 用 b 個 bits 的二進位去做表示。並且要記得加上前面在做擴增動作時，已經確定的 ciphertext。

## Adaptive Algorithm - Decoding

假設 data set 有 M 個值（ex: 1, 2, ..., M），因此 initial probability 設定為 uniform 的：

```python
dic = {'total':0}
for s in set:
    dic[s] = 1
    dic['total'] += 1
```

接著，decoding 的演算法與前面相同，只是每次 for loop 開始時，都要先重新計算過一次 inteval of probability，並且在 for loop 的最後要對 dic 去做更新。

```python
def inteval(dic):
    S = {}
    for k in dic.keys():
        if k != 'total':
            S[k] = [prev, prev + dic[k]/dic['total']]
            prev += dic[k]/dic['total']
    return S

lower, upper = 0, 1
lower1, upper1 = 0, 1
j = 0
for i in range(N):
    S = inteval(dic)
    check = True
    while check:
        exist = False
        for k in S.keys():
            if lower + (upper-lower) * S[k][0] <= lower1 and lower + (upper-lower) * S[k][1] >= upper1:
                check = False
                exist = True
        if not exist:
            lower1 = lower1 + (ciphertext[j-1]+1) * 2**(-j)
            upper1 = lower1 + ciphertext[j-1] * 2**(-j)
    text += n
    lower = lower + (upper-lower) * S[k][0]
    upper = upper + (upper-lower) * S[k][1]
    dic[k] += 1
    dic['total'] += 1
```

然後在 decoding 的過程中，一樣注意 floating point error 的發生，同時對 lower & upper bound 以及 lower1 & upper1 bound 去做擴增。

## Context-Modeling

## Performance - Arithmetic Coding

* **lower & upper bound update**：
    set = ['a', 'b'], probability = [0.8, 0.2], text = 'aaabaa'

    ![](https://i.imgur.com/5F5Ir54.jpg)

* **Simple Coding**

    ![](https://i.imgur.com/B4TTMmr.jpg)

* **Different Length of Data**

    ![](https://i.imgur.com/zlfmobg.jpg)

* **Different Distribution of Data**

    ![](https://i.imgur.com/ZqcNTdt.jpg)

## Performance - Adaptive Arithmetic Coding

* **Simple Coding**

    ![](https://i.imgur.com/3TPP2Cx.jpg)

* **Different Length of Data**

    ![](https://i.imgur.com/twvDaNu.jpg)

* **Different Distribution of Data**
* 
    ![](https://i.imgur.com/DoNJrMb.jpg)


## Performance - Context-Modeling Adaptive Atihmetic Coding

* **Sentence Coding**

    ![](https://i.imgur.com/0mZa5D2.jpg)

* **Articles Coding**

    ![](https://i.imgur.com/MfaPwgE.jpg)

* **Normal Distribution Coding**

    ![](https://i.imgur.com/rNdaIlJ.jpg)

## Usage

* 執行 `main.py`，會得到下圖的 command

    ![](https://i.imgur.com/q0Hdm1X.jpg)

* 接著輸入 `0` 進入一般的 Arithmetic Coding；輸入 `1` 進入 Adaptive Arithmetic Coding；輸入其他則會出現 error

    ![](https://i.imgur.com/ftYLtvN.jpg)

    ![](https://i.imgur.com/oXyqr6V.jpg)

> 若要更改 data set 或是 probability of data 的話，請事先進入 `main.py` 進行編輯

* 進入兩種 mode 之後，輸入 text message，就會根據選擇的 mode 做 encoding & decoding。

    ![](https://i.imgur.com/8B2SeXC.jpg)

* 如果想要換模式，則輸入 `change` 可以換模式。

    ![](https://i.imgur.com/VcLuBii.jpg)

* 如果想要離開，則輸入 `quit` 可以離開。

    ![](https://i.imgur.com/hp3tMtS.jpg)

## Demo

[Demo Video](https://www.youtube.com/watch?v=RhH3OKNkydk&ab_channel=0314Patrick)


###### tags: `Github`
