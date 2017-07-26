 # pySPR - Symbolic Pattern Recognition in Python

## This code implements the Symbolic Pattern Recognition (SPR) methods as published by:

- Akbilgic O and Howe J. *Symbolic Pattern Recognition for Sequential Data*. Sequential Analysis. Accepted for publication.
- Akbilgic, O., Howe, J. A., Davis, R. L., December 2016. [*Categorizing Atrial Fibrillation via Symbolic Pattern Recognition*](http://hoajonline.com/medicalstat/2053-7662/4/8#). Journal of Medical Statistics and Informatics 4 (8), 1–9.

Everything was developed from first principals and the documentation in the articles. This code was not simply ported from the original MATLAB source code.

Several optimizations have been used, including efficient hash-based substring search and several recurrence relations between sequentially-sized lists of n-grams and pattern transition matrices.

## Demonstrating Usage:
### Create the SPR analysis object:
`thisSPR = SPRanal(['a','b','c'],'aabcabccbabcabcbaabc')`

### Set it up for the modeling - this must be done before anything else
`thisSPR.SetPTPParams(10,0.1,{'p':4241,'x':42}); print(thisSPR)`

### Functions (used by `BuildPTPs`) to generate specified ngrams and PTP matrices
`ngrams_2 = thisSPR.MakenGrams(maxn_p=2,only=True)`

`PTP_2 = thisSPR.BuildPTP(ngrams_2,ngramsRed=None)[0]`

`print(thisSPR.PrintPTP(PTP_2,ngrams_2,True))`

### Identify the optimal `n_p` and set the PTP matrices 
`thisSPR.BuildPTPs(True); print(thisSPR.PrintiPTP(1))`

### Predict the next symbol, and simulate a similar sequence
`print('The next symbol should be: %s'%thisSPR.Predict(predStart=None)[0])`

`print('A similar sequence is: %s'%thisSPR.Simulate(20))`

### Compute the distances between some sequences
`SstarSPR = SPRanal(thisSPR.alpha,'abcbaabcabccbabcabcb')`

`SstarSPR.SetPTPParams(10,0.1,{'p':4241,'x':42}); SstarSPR.BuildPTPs(True)`

`SstarstarSPR = SPRanal(thisSPR.alpha,'bcbabcbaababcbababcc')`

`SstarstarSPR.SetPTPParams(10,0.1,{'p':4241,'x':42}); SstarstarSPR.BuildPTPs(True)`

`print('dist(S,S*) = %0.2f'%thisSPR.Distance(SstarSPR))`

`print('dist(S,S**) = %0.2f'%thisSPR.Distance(SstarstarSPR))`

`print('dist(S*,S**) = %0.2f'%SstarSPR.Distance(SstarstarSPR))`
