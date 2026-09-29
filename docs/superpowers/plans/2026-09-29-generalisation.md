# Généralisation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Compléter la section 3 de `1 - Qu'est-ce qu'apprendre ?.md` avec 3 sous-sections intuitives sur par cœur vs généraliser.

**Architecture:** Modification unique d'un fichier markdown existant, en 3 blocs (3.1, 3.2, 3.3) + exercice, avec callouts Obsidian et embeds existants, sans nouveau script ni théorie formelle.

**Tech Stack:** Markdown Obsidian (wiki links, callouts, embeds), YAML frontmatter strict, assets PNG existants (réutilisation seule, aucune génération nouvelle per spec hors-scope).

---

### Task 1: Structurer la section 3 vide

**Files:**
- Modify: `cours_ml/1 - Qu'est-ce qu'apprendre ?.md:78-89`
- Test: vérification via `rg` des titres

- [ ] **Step 1: Lire la section actuelle pour ancrer l'edit**

```bash
sed -n '78,89p' "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"
```
Expected: montre `# 3. Apprentissage supervisé : tentative de généralisation` + image `Pasted image 20260928145826.png`

- [ ] **Step 2: Insérer les 3 sous-titres + callouts vides**

Remplacer le bloc après l'image par:

```markdown
# 3. Apprentissage supervisé : tentative de généralisation

![[Pasted image 20260928145826.png|398]]

## 3.1 Apprendre par cœur VS généraliser

> [!example] À compléter en tâche 2
> Contenu polynômes.

## 3.2 Qu'est-ce que généraliser ?

> [!info] À compléter en tâche 2
> Définition train/test.

## 3.3 Comment valider sans se mentir ? (hold-out)

> [!danger] À compléter en tâche 2
> Protocole.
```

- [ ] **Step 3: Vérifier les titres**

Run: `rg -n "^## 3\.[123]" "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"`
Expected: 3 lignes `## 3.1`, `## 3.2`, `## 3.3`

- [ ] **Step 4: Commit**

```bash
git add "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"
git commit -m "docs: structure section 3 généralisation en 3 sous-parties"
```

### Task 2: Rédiger 3.1 + 3.2 + 3.3 (intuitif, polynômes)

**Files:**
- Modify: `cours_ml/1 - Qu'est-ce qu'apprendre ?.md:78-130`
- Test: `rg` vocabulaire + absence de formules interdites

- [ ] **Step 1: Écrire le contenu 3.1 Par cœur vs généraliser**

Remplacer le placeholder `[!example]` par:

```markdown
> [!example] Par cœur vs tendance (régression polynomiale)
> - Mêmes points bruités autour d'une courbe douce.
> - Degré 1 : rate partout (sous-apprentissage).
> - Degré 4 environ : capte la tendance, petite erreur train stable.
> - Degré 15 : passe par tous les points, erreur train = 0 mais zigzague au moindre bruit = par cœur.
> Retenir : erreur train 0 ne prouve rien, c'est même suspect.
```

- [ ] **Step 2: Écrire le contenu 3.2 Définition généraliser**

Remplacer placeholder `[!info]` par:

```markdown
> [!info] Généraliser = être bon sur du non-vu
> Généraliser = erreur faible sur des données **non vues** à l'entraînement.
> Vocabulaire : **erreur train** (sur données d'entraînement) vs **erreur test** (sur données gardées de côté, split train/test).
> Schéma : train -> entraîne, test verrouillé -> juge.
```

- [ ] **Step 3: Écrire le contenu 3.3 Validation hold-out**

Remplacer placeholder `[!danger]` par:

```markdown
> [!danger] Ne jamais juger sur le train seul
> Protocole hold-out : 1) couper le jeu en train/test, 2) entraîner sur train seul, 3) mesurer une fois sur test verrouillé.
> Le test ne sert pas à régler le modèle, sinon il devient du train déguisé.
> Suite : complexité et courbe en U en [[3- Données non linéairement séparables#4. Complexification des modèles et impact sur la généralisation|partie 4]], validation croisée et surapprentissage en partie 7.
```

- [ ] **Step 4: Vérifier vocabulaire et absence de théorie formelle**

Run: `rg -n "erreur train|erreur test|hold-out|par cœur" "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"`
Expected: >=4 matchs dans section 3

Run: `rg -n "Hoeffding|VC|PAC|Rademacher|borne" "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"`
Expected: aucun match (niveau intuitif seulement)

- [ ] **Step 5: Commit**

```bash
git add "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"
git commit -m "docs: rédige 3.1-3.3 généralisation intuitive polynômes"
```

### Task 3: Exercice + liens + vérification Obsidian

**Files:**
- Modify: `cours_ml/1 - Qu'est-ce qu'apprendre ?.md:fin section 3`
- Test: `rg` liens + frontmatter check

- [ ] **Step 1: Ajouter l'exercice et les liens finaux**

Ajouter à la fin de la section 3:

```markdown
> [!question] Pourquoi 100% sur le train ne prouve rien ?
> Donnez un contre-exemple de modèle par cœur (table de mémorisation ou polynôme degré 15) qui a 0 erreur train mais échoue sur test. Que faudrait-il mesurer pour trancher ?
```

- [ ] **Step 2: Vérifier frontmatter inchangé et liens valides**

Run: `sed -n '1,10p' "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"`
Expected: bloc `---` avec `titre:`, `cours: "[[Entrypoint]]"`, `Contexte: |-`

Run: `rg -n "\[\[.*\]\]" "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"`
Expected: contient `[[Entrypoint]]` et lien vers partie 4, aucun `[[...]]` cassé évident

- [ ] **Step 3: Vérifier longueur et rendu**

Run: `wc -l "cours_ml/1 - Qu'est-ce qu'apprendre ?.md" && rg -c "^> \[!" "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"`
Expected: +30 à +60 lignes vs origine (~89 -> ~120-150), >=5 callouts

- [ ] **Step 4: Commit**

```bash
git add "cours_ml/1 - Qu'est-ce qu'apprendre ?.md"
git commit -m "docs: exercice et liens généralisation section 3"
```
