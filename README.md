# Arithmetic Coding

Arithmetic coding 則是將多筆資料一起編碼，近年來的資料壓縮技術大多使用 Arithmetic coding，壓縮效率比 Huffman coding 更高。

## Algorithm - Encoding

統計 data 中每筆資料的出現機率 p，接著計算每筆資料的機率區間 S：

> ![](https://i.imgur.com/9zIzgvJ.png)

接著根據 Arithmetic Coding 的演算法來更新 lower bound and upper bound：

> ![](https://i.imgur.com/SwUvGy0.png)

最後假設：
> ![](https://i.imgur.com/7t43qQj.png)

其中 C 和 b 皆為整數，且 b 越小越理想。

找出 C 和 b 之後，data x 的編碼則是用 k 進位 b bits 來表示 C。

> ![](https://i.imgur.com/d03j5BP.png)

## Algorithm - Decoding

## Performance

## Usage
