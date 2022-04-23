# Arithmetic Coding

Arithmetic coding 則是將多筆資料一起編碼，近年來的資料壓縮技術大多使用 Arithmetic coding，壓縮效率比 Huffman coding 更高。

## Algorithm - Encoding

統計 data 中每筆資料的出現機率 p，接著計算每筆資料的機率區間 S：

```python
S = [0]
for p in P:
    S.append(S[-1]+p)
```

接著根據 Arithmetic Coding 的演算法來更新 lower bound and upper bound：

```python
# Initial
lower, upper = S[X[0]], S[X[0]+1]

# Update
for x in X:
    lower = lower + S[x] * (upper - lower)
    upper = lower + S[x+1] * (upper - lower)
```

當 length of data 不長的時候可以用上面的方法，但是當 length of data 太長的時候，直接更新 lower bound 或是 upper bound 最後會造成 floating point error。

對此我們使用一個小技巧，當 lower bound ＞ 0.5 的時候，可以判斷說 ciphertext 會增加一個 `1`，又或是當 upper bound ≦ 0.5 的時候，可以判斷說 ciphertext 會增加一個 `0`。因此可以將上面的方法改成：

```python
ciphertext = ''
for x in X:
    lower = lower + S[x] * (upper - lower)
    upper = lower + S[x+1] * (upper - lower)
    
    while lower > 0.5 or upper <= 0.5:
        if lower > 0.5:
            ciphertext += '1'
            lower = lower * 2 - 1
            upper = upper * 2 - 1
        elif upper <= 0.5:
            ciphertext += '0'
            lower = lower * 2
            upper = upper * 2
```

經過改良後，可以確保 lower bound 與 upper bound 的數值差不會太小，並且可以縮短找 C 和 b 的 time cost。最後假設：
```
lower <= C * k^(-b) < (C+1) * k^(-b) <= upper
```
其中 C 和 b 皆為整數，且 b 越小越理想。

找出 C 和 b 之後，data x 的編碼則是用 k 進位 b bits 來表示 C。

```
Ex: k = 2, b = 5, C = 14
  → C(b, k) = 01110
```

## Algorithm - Decoding

假設原始的 lower bound 跟 upper bound，並且假設 encoding 後的 C 和 b 的 lower bound 1 跟 upper bound 1。

從 ciphertext 的右側開始掃描，依次更新 lower bound 1 & upper bound 1。如果 ciphertext = `0`，代表說 bound range 1 在原範圍的 0-0.5 之中；反之如果 ciphertext = `1`，則代表說 bound range 1 在原範圍的 0.5-1 之中。

接著判斷說 recovered text 是否可以有確定的值，也就是 lower bound & upper bound 是否包含了 lower bound 1 和 upper bound 1。

也就是更新 lower bound & upper bound 的同時，如果發現沒有確定的 recovered text 時，更新 lower bound 1 & upper bound 1。

另外，為了避免 lower bound 和 upper bound 出現 floating point error，當 lower bound > 0.5 或是 upper bound ≦ 0.5 的時候，同樣要做倍數的運算。此時，要連動 lower bound 1 & upper bound 1 做相同的運算。

```python
lower, upper = 0, 1
lower1, upper = 0, 1
j = 1
X = ''
for i in range(N):
    check = True
    while check:
        for_break = True
        for n in range(len(S)):
            if lower + inteval[n] * (upper-lower) <= lower1 and upper + inteval[n+1] * (upper-lower) > upper1:
                for_break, check = False, False
                break
        if for_break:
            lower1 = lower1 + ciphertext[j] * 2**(-j)
            upper1 = upper1 + (ciphertext[j]+1) * 2**(-j)
            
    X += set[n]
    lower = lower + inteval[n] * (upper-lower)
    upper = lower + inteval[n+1] * (upper-lower)
    
    while lower > 0.5 or upper <= 0.5:
        if lower > 0.5:
            lower = lower * 2 + 1
            upper = upper * 2 + 1
            lower1 = lower1 * 2 + 1
            upper1 = upper1 * 2 + 1
        if upper <= 0.5:
            lower *= 2
            upper *= 2
            lower1 *= 2
            upper1 *= 2
```

## Performance

* lower bound 和 upper bound 的更新：

    set = ['a', 'b'], probability = [0.8, 0.2]
    
    text = 'aaabaa'

    ![](https://i.imgur.com/5F5Ir54.jpg)

* 比較不同的 set 跟 probability distibution：
    
    ![](https://i.imgur.com/O1FfDLB.jpg)

    
* 比較不同的 length of data：

    ![](https://i.imgur.com/8GaDDYd.jpg)

## Usage

* 執行 `main.py`，會得到下圖的 command

![](https://i.imgur.com/l3BDRIk.png)

* 原本的 default data set 和 default probability 如同圖中所示，如果有需要更改的話可以從 `main.py` 中更改。

  確保 `len(set) == len(probability)` & `sum(probability) == 1`，不然會產生 error。

* 如果不須更改 data set 或是 data probability，抑或是更改完後，直接輸入想要做 encoding 的 data string。

![](https://i.imgur.com/zqKl9EH.png)

* 按下 `enter` 之後，會 output 出 encoding + decoding 的時間，並且輸出 encoded ciphertext 以及 recovered text。

![](https://i.imgur.com/yXYCNPb.png)

* 如果想要退出程式，則輸入 `quit` 就會自動結束

![](https://i.imgur.com/2MoTh8r.png)

###### tags: `Github`
