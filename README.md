# pySPR
My semi-optimized SPR implementation in Python

This code implements the Symbolic Pattern Recognition (SPR) methods as published by:

  Akbilgic O and Howe J. Symbolic Pattern Recognition for Sequential Data. 
    Sequential Analysis. Accepted, awaiting publication.
  Akbilgic, O., Howe, J. A., Davis, R. L., December 2016. Categorizing Atrial 
    Fibrillation via Symbolic Pattern Recognition. Journal of Medical Statistics 
    and Informatics 4 (8), 1–9.

Everything was developed from scratch, first principals, and reading the documentation in the articles. This code was not simply ported from the original MatLab.

Several optimizations have been used, including efficient hash-based substring search and several recurrence relations between sequentially-sized lists of ngrams and pattern transition matrices.

To demonstrate, after loading the required modules and the SPRanal class, run this code:

'''
SPR Analysis Demo Code, using same example as in the original article
'''
# create the SPR analysis object
thisSPR = SPRanal(['a','b','c'],'aabcabccbabcabcbaabc')
print(thisSPR)
# set it up for the modeling - this must be done before anything else
# from Section 3.1 Learning Pattern Transition Behaviour of the original article
thisSPR.SetPTPParams(10,0.1,{'p':4241,'x':42})
print(thisSPR)

# functions (used by BuildPTPs) to generate specified ngrams and PTP matrices
ngrams_2 = thisSPR.MakenGrams(maxn_p=2,only=True)
PTP_2 = thisSPR.BuildPTP(ngrams_2,ngramsRed=None)[0]
print(thisSPR.PrintPTP(PTP_2,ngrams_2,True))

# identify the optimal n_p and set the PTP matrices 
thisSPR.BuildPTPs(True)
print(thisSPR.PrintiPTP(1))

# predict the next symbol, and simulate a similar sequence; these are from sections
# 3.2 SPR for Prediction and 3.3 Simulating with SPR, respectively
print('The next symbol should be: %s'%thisSPR.Predict(predStart=None)[0])
print('A similar sequence is: %s'%thisSPR.Simulate(20))

# compute the distances between some sequences; these are from section
# 3.4 Clustering with SPR
SstarSPR = SPRanal(thisSPR.alpha,'abcbaabcabccbabcabcb')
SstarSPR.SetPTPParams(10,0.1,{'p':4241,'x':42})
SstarSPR.BuildPTPs(True)

SstarstarSPR = SPRanal(thisSPR.alpha,'bcbabcbaababcbababcc')
SstarstarSPR.SetPTPParams(10,0.1,{'p':4241,'x':42})
SstarstarSPR.BuildPTPs(True)
print('dist(S,Sst) = %0.2f'%thisSPR.Distance(SstarSPR))
print('dist(S,Sstst) = %0.2f'%thisSPR.Distance(SstarstarSPR))
print('dist(Sst,Sstst) = %0.2f'%SstarSPR.Distance(SstarstarSPR))
