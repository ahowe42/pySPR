# pySPR - Symbolic Pattern Recognition in Python

This code implements the Symbolic Pattern Recognition (SPR) methods as published by:
- Akbilgic O and Howe J. Symbolic Pattern Recognition for Sequential Data. Sequential Analysis. Accepted, awaiting publication.
- Akbilgic, O., Howe, J. A., Davis, R. L., December 2016. Categorizing Atrial Fibrillation via Symbolic Pattern Recognition. Journal of Medical Statistics and Informatics 4 (8), 1–9.

Everything was developed from first principals and the documentation in the articles. This code was not simply ported from the original MatLab.

Several optimizations have been used, including efficient hash-based substring search and several recurrence relations between sequentially-sized lists of ngrams and pattern transition matrices.
