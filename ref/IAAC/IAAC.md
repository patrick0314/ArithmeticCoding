# IAAC

## Ⅰ.Introduction

Huffman code 因為是 encode each input separately，所以在 coding efficiency 上不如 Arithmetic coding 來的有效率。

Arithmetic coding 可以簡單分成兩類：

* **Static Arithmetic Coding (SAC)**:
    根據給定的 probability distribution，去判斷每個 input data 對應的 range。每次更新 lower & upper bound，接著更新 range。最後，用 serier of bits 來代表 range [L, H]。
    這個方法需要額外紀錄 estimated probability of the input data。

* **Adaptive Arithmetic Coding (AAC)**:
    不需要紀錄 probability distribution，而是利用 frequency table，對每個 input data 都去更新 table，接著用 table 來當作 distribution 來做 encoding。
    由於不需要額外的 data 來記錄，因此 AAC 比 SAC 有更高的 coding efficiency。

CAAC 被廣泛應用在 text compression 以及 lossy / lossless image compression。此外，像是 MQ coder 則是一種 entropy coding，被應用在 JPEG2000，可以看成是 SAC 跟 CAAC 的結合，是根據 input signal 來做 table switching。還有像是 CABAC 是被應用在 video coding 以及 HEVC standard。

這篇演算法主要是針對 AAC & CAAC 的改進，雖然這兩個方法已經有很高的 compression ratio，但是相信還是有改進空間。像是當 X = v 的時候，只會針對 Fc[v] 去做 update，但是一些與 v 相關性極高的 data 就沒有考慮到；又或是當 context C 時，只會對 Fc table 去做 updata，但如果 C1 和 C 的相關性極高，應該也會有類似的 probability distribution。

## Ⅱ.Improvement for Adaptive Arithmetic Coding

* **Initialization of the Frequency Table**
    並非像是 SAC 一樣的需要 probability distribution of input data，也不是像 AAC 一樣的去做 uniformly initialization。而是跟去一些 probability model 去做假設，像是 Gaussain model 或是 exponential model。
    
    比起 F[v] = 1 的廣泛假設，這些 probability model 有更貼近的 distribution，因此能夠有更好的 compression performance，尤其對於一開始的 input data。

* **The Range-Adjusting Scheme**
    當 n-th input X[n] = v 時，不單單只是針對 F[v] 去做 update，針對與 P(X[n]=v) 有高度相關性的 P(X[n]=u)，F[u] 也要同時做 update。
    
    $F[v_1] ← F[v_1] + A * B[v, v_1] \quad \text{if} \ \ X[n]=v$
    
    * $B[v, v_1]$ 隨著 $v$ 和 $v_1$ 的差異越大而減少
    * $\Sigma \ B[v, v_1] = 1$

    最常見的 B function 就是 rectangular function form。也可以是 exponential function form 或是 normalized exponential function form。
    
    原始的 AAC 只能在 input data 足夠長時，才能保證 compression performance，但是當使用了此方法之後，由於 rapid convergence，因此可以大幅的提升 coding performance。

* **The Increasingly Adjusting Step**
    傳統的 AAC 在做 update 的時候，adjusting step 都是固定為 1，這樣的意義代表說每個 input data 對於 frequency table 都有相同的影響力，但是通常的情況都不會是這樣。
    
    因此我們將 adjusting step 改變成：
    
    $F[v] ← F[v] + A[n] \quad \text{if} \ \ X[n]=v$
    
    * $A[n-k_1] > A[n-k_2] \quad \text{if} \ \ k_1 < k_2$
    
    上述的條件是為了確保，當在 encoding n-th input data 時，(n-k1)-th input 會比 (n-k2)-th input 有更大的影響力。
    
    常見的 function 有 linear form 或是 geometric form。前者適合 short input case，後者則適合 long input case。
    
    另外，為了避免 frequency table 和 adjusting step 變得過度 large，因此當 $\Sigma \ F[v]$ 超過一定的 threshold，就會進行 scaling 和 quantization operation。
    
    $F[v] ← \text{Max}(F[v]/2, \delta)\quad  \text{and} \quad A[v] ← A[v]/2 \quad \text{if} \ \ \Sigma \ F[v] > T$
    
    這樣就可以確保說 $F[v]/\text{sum}(F[v])$ 永遠不會小於 $\delta/T$。
    
    如果要結合 the increasingly adjusting step 和 range-adjusting scheme，則是將 formula of frequency table 改成：
    
    $F[v_1] ← F[v_1] + A[n]B[v, v_1] \quad \text{if} \ \ X[n]=v$

* **The Mutual-Learning Scheme**
    此方法是針對 context modeling 去做改進。$F_j[v]$ 以及 $F_q[v]$ 分別是對應到 j-th context 以及 q-th context。如果 j-th context 和 q-th context 有高度的相關性，可以合理推測兩者會有類似的 probability distribution。因此在對 $F_j[v]$ 做 update 的時候，應該也要對 $F_q[v]$ 做調整。
    
    當 $X[n] = v$ 時，j-th context 的 frequency table 的 update 應該是：
    
    $F_j[v_1] ← F_j[v_1] + A[n]B[v, v_1]$
    
    此外，q-th context 的 frequency table 應該也要做調整：
    
    $F_q[v_1] ← F_q[v_1] + A[n]B[v, v_1]C[j, q]$
    
    * $C[j, q]$ 介於 0 - 1

* **The Local Frequency Table**
    除了 initial table 之外，另外建立一個 local frequency table，在 initial table 不斷被更新的時候，如果我們可以確定說這些 data 有一定的規律，則可以根據這些規律去對 initial table 做變化，讓 frequency table 更符合想要情境。
    
    如果我們可以確定說 $F[v]$ 應該有更高的 frequency：
    
    $F_L[v] = \rho[v]F[v], \quad \rho[v]>1$
    
    當 $F[v] 超過 usual case 之後：
    
    $F_L[v] = F[v] \quad \text{otherwise}$
    
    這樣可以避免一些 data 在各種極端值或是分散不均時會有 error。

雖然引進的很多新的方法，但是 proposed AAC 依然保持了 linear to the input data size。其中 initializing the frequency、increasing the adjusting step、the local frequency table 對於 computation time 都沒有什麼影響。而 range-adjusting scheme 和 mutual-learning 則可以依靠 table loopup 來節省時間。

## Ⅲ.Applications

* **Example for EDP Lossless Image Compression**
    

* **Encoding DC and AC Terms in JPEG**
    * DC differences
    * AC Coefficients

* **Example for JPEG2000**
    

* **Example for Motion Vector Difference Encoding in Video Compression**
   

###### tags: `Paper`