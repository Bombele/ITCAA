# Module Legal – Guide

## 🎯 Objectif
La branche `feature/legal` est dédiée au **développement, expérimentation et durcissement des mécanismes de conformité juridique et normative**.  
Elle permet de tester, valider et améliorer les cadres légaux, le droit numérique et le droit international humanitaire (DIH) avant leur intégration officielle dans la branche principale `itcaa/`.

---

## 📂 Structure des fichiers

- **legal_framework/**  
  Cadres juridiques et normatifs.  
  - `legal_framework_fr.md` → version française.  
  - `legal_framework_en.md` → version anglaise.  
  - `legal_framework_ar.md` → version arabe.  
  - `legal_framework_sw.md` → version swahili.  
  - `legal_framework_ln.md` → version lingala.  
  - `legal_framework.py` → moteur de validation des normes juridiques.

- **compliance/**  
  Modules de conformité et vérification.  
  - `compliance_checker.py` → vérification conformité légale et réglementaire.  
  - `compliance_rules.json` → règles et standards juridiques.  
  - `compliance_fr.md`, `compliance_en.md`, `compliance_ar.md`, `compliance_sw.md`, `compliance_ln.md` → documentation multilingue.

- **dih/**  
  Droit international humanitaire.  
  - `dih_protocols_fr.md` → version française.  
  - `dih_protocols_en.md` → version anglaise.  
  - `dih_protocols_ar.md` → version arabe.  
  - `dih_protocols_sw.md` → version swahili.  
  - `dih_protocols_ln.md` → version lingala.  
  - `dih_checker.py` → vérification conformité DIH.

- **tests/**  
  - `test_legal_framework.py` → Vérifie la robustesse du moteur juridique.  
  - `test_compliance.py` → Vérifie la validité des règles de conformité.  
  - `test_dih.py` → Vérifie la conformité aux protocoles DIH multilingues (FR/EN/AR/SW/LN).

---

## 🧪 Tests
- **Unitaires** : validation des fonctions de conformité et de vérification juridique.  
- **Intégration** : cohérence entre cadre légal, conformité et DIH.  
- **Multilingue** : vérification des traductions et cohérence des documents (FR/EN/AR/SW/LN).  

---

## 🧭 Gouvernance et impact institutionnel
- **Expérimentation contrôlée** : la branche `feature/legal` sert de laboratoire pour tester les mécanismes juridiques.  
- **Traçabilité** : chaque modification est documentée dans la Bitácora.  
- **Institutionnalisation** : une fois validés, les modules sont fusionnés dans `itcaa/`.  
- **Impact** : garantit la conformité légale, la robustesse normative et le respect du DIH avant adoption officielle par les institutions africaines.  

---

## ✅ Conclusion
La branche `feature/legal` est le **laboratoire technique et normatif d’ITCAA pour le droit numérique et le DIH**.  
Elle permet de tester et durcir les cadres juridiques et protocoles multilingues (FR/EN/AR/SW/LN) avant leur intégration institutionnelle dans la branche principale `itcaa/`.