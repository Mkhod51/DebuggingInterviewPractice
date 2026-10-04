# Debugging explanation template

1. **Symptom:** Which user behavior or test failed? What was actually observed?
2. **Expected behavior:** Which README rule establishes the correct result?
3. **Hypothesis:** What could produce the difference? What competing explanation remains?
4. **Evidence:** What input, trace, assertion or state comparison tests the hypothesis?
5. **Root cause:** What incorrect assumption causes the behavior, and where does it enter?
6. **Correction:** What changed, why is it sufficient, and what healthy behavior is preserved?
7. **Verification:** Which original and additional cases were run? What is still untested?

Spoken draft: “I reproduced ___ with ___. The contract requires ___. I suspected ___
and checked ___; I observed ___. The cause was ___. I changed ___ and verified ___,
including ___. I have not yet checked ___.” Replace every blank with evidence, and
omit the final uncertainty clause only if there is no material uncertainty to mention.
