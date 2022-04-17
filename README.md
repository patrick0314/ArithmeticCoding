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

最後假設：
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

## Performance

* `data set = ['a', 'b']`  `data_length = 10`

![](https://i.imgur.com/Uxdtdlq.png)

![](https://i.imgur.com/5JkBllv.png)

![](https://i.imgur.com/E1oul3e.png)

* `data set = ['a', 'b']`  `data_length = 20`

![](https://i.imgur.com/BuzVs30.png)

![](https://i.imgur.com/J0qsMnF.png)


## Usage

* 執行 `main.py`，會得到下圖的 command

![](https://i.imgur.com/l3BDRIk.png)

* 原本的 default data set 和 default probability 如同圖中所示，如果有需要更改的話可以從 `main.py` 中更改。

* 如果不須更改 data set 或是 data probability，抑或是更改完後，直接輸入想要做 encoding 的 data string。

![](https://i.imgur.com/zqKl9EH.png)

* 按下 `enter` 之後，會 output 出 encoding + decoding 的時間，並且輸出 encoded ciphertext 以及 recovered text。

![](https://i.imgur.com/yXYCNPb.png)

* 如果想要退出程式，則輸入 `quit` 就會自動結束

![](https://i.imgur.com/2MoTh8r.png)

###### tags: `Github`
