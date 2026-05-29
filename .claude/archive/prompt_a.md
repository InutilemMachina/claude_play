---
title: Prompt A — Claude Project Custom Instructions (ELAVULT)
type: prompt-archived
archived: 2026-05-29
reason: Aktualitása kérdéses; a CLAUDE.md és Instructions.md lefedi a szerepkör-leírást. Az NLM-specifikus forráskezelési szabályok Prompt B-be integrálódtak.
---

# Prompt A — Claude Project Custom Instructions

**Hova:** Claude Desktop → Cowork Instructions mező (vagy Project Instructions)

**Mikor:** Egyszeri setup — a `.claude/CLAUDE.md` tartalmával együtt másolandó be.

```
# SOURCE RECONCILIATION & FILE EXTENSION POLICY

1. EXTENSION MAPPING: NotebookLM preserves file extensions for uploaded documents (e.g., "tavak2004.pdf") and strips them for web URLs. Cross-reference source names from NLM JSON responses with the project knowledge base.
2. RESOLVE SHORTHAND NAMES: When NLM CLI returns a source name, expand it into a full bibliographic citation for the Bibliography section of the output document.
3. CITATION JSON MAPPING: The CLI response contains a "citations" dict (citation number → source UUID) and a "references" list (UUID + cited text). Use these to build the citations.json file in step 04_citations_maker.

# INFERRED VISUALS & AUDIT TRAIL RECONSTRUCTION

1. HEURISTIC PROCESSING: If NLM returns an implicit anchor (e.g., "Figure 2", unnamed diagram), translate it into a readable, traceable reference in the final document.
2. DUAL-INDEX CITATION SYSTEM: Format citations to include both the human-readable citation and the machine-verifiable source link.
3. MISSING CONTEXT DETECTOR (3-ROUND RECOVERY): If NLM returns a table but the surrounding context is vague, run a targeted follow-up via: nlm query notebook "<ID>" "<follow-up question>" --conversation-id <id> --json — up to 3 rounds before compiling the final document.

# FINAL OUTPUT VERIFICATION

Every table cell with numerical data and every image/chart mention must trace back to:
* The exact source filename (with extension).
* The specific page, paragraph, or contextual anchor from NotebookLM.
* The corresponding bibliography entry at the end of the Markdown file.
```
