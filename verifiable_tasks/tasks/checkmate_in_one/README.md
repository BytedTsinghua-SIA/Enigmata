# Checkmate In One Move

This task asks models to find a move in the chess position resulting in checkmate.

**Author:** Nitish Shirish Keskar (nkeskar@salesforce.com)

The goal of this task is to probe the ability of language models to play chess in [standard algebraic notation (SAN)](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)). The input to the model is a sequence of moves such that a next possible move is a checkmate. We curate 3,500 games and measure the performance of the system in exact match accuracy.

``` 
1. e4 e6 2. Ke2 d5 3. e5 c5 4. f4 Nc6              
5. Nf3 Qb6 6. g4 Bd7 7. h4 Nge7 8. c3 Ng6          
9. d4 cxd4 10. cxd4 Be7 11. Kf2 O-O 12. h5 Nh8              ----------->   Bxh7#
13. Be3 Qxb2+ 14. Kg3 Qxa1 15. Bd3 Qxa2 16. Rh2 Qa1
17. Qc2 Nb4 18.               
```

You can download the dataset from [BIG-Bench](https://github.com/google/BIG-bench/tree/092b196c1f8f14a54bbc62f24759d43bde46dd3b/bigbench/benchmark_tasks/checkmate_in_one)