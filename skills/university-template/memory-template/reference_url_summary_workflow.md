---
name: URL processing — ALWAYS goes through {{PROJECT_NAME}}/university/ pipeline
description: CRITICAL. User has a full Zettelkasten knowledge base at {{PROJECT_PATH}}/university/. Every URL they give must be processed through METHODOLOGY.md pipeline — not chat-style summaries.
type: reference
---

**If the user pastes ANY URL (article, paper, YouTube, docs, thread), the default action is: process it into `{{PROJECT_PATH}}/university/`.** Not a chat summary. Not an ad-hoc response. Full pipeline.

Skip the pipeline ONLY if user explicitly says "просто перескажи" / "не в университет" / "быстрый пересказ".

## Locations to read FIRST

1. `{{PROJECT_PATH}}/university/README.md` — entry point
2. `{{PROJECT_PATH}}/university/METHODOLOGY.md` — the rules, read before every new URL
3. `{{PROJECT_PATH}}/university/TAXONOMY.md` — in/out of scope filter (§2)
4. `{{PROJECT_PATH}}/university/INDEX.md` — what's already processed (dedup check)
5. `{{PROJECT_PATH}}/university/_templates/` — use these templates verbatim

## Pipeline (from METHODOLOGY.md §4) — do every step, in order

```
URL
 ├─ 1. Fetch        → sources/<src-id>/original.<ext> + meta.yaml
 ├─ 2. Relevance    → score 0-5 against TAXONOMY §2. If 0 → sources/_rejected/
 ├─ 3. Quality      → score 0-10 per METHODOLOGY §3 checklist
 ├─ 4. Conspect     → sources/<src-id>/conspect.md (format in §6)
 ├─ 5. Atomize      → notes/n-<slug>.md × N (rules §7)
 ├─ 6. Claims       → claims/c-<NNNN>.md × M (format §8)
 ├─ 7. Link extract → queue/to-follow.md (all outbound URLs)
 ├─ 8. Synthesis    → update syntheses/<topic>.md if picture changed (§9)
 ├─ 9. Graph        → append edges to graph/edges.jsonl
 └─10. Index        → add/update row in INDEX.md
```

## ID conventions (METHODOLOGY §11)

- Source: `src-YYYYMMDD-<slug>` (use today's date, NOT publication date)
- Note: `n-<slug>` (3-5 words kebab-case, title is a statement not a topic)
- Claim: `c-<NNNN>` zero-padded, next available from INDEX
- Synthesis: `syn-<taxonomy-leaf>`
- Contradiction: `contr-<NNN>`
- Verdict: `v-<slug>`

## Idempotency

Check `INDEX.md` and canonical URLs (strip utm_*, fbclid, ref=, etc.) of existing `sources/*/meta.yaml` before creating a new source. Reuse existing source_id if match.

## BFS depth & limits (§5)

- Max depth 3 from user's root URL
- Per session cap: 50 new sources per root
- At each depth, only follow links with predicted relevance ≥ 2
- Dedup via canonical URL + `graph/edges.jsonl`

## YouTube specifically

For YouTube URLs the pipeline is:
1. Get transcript via any available method — check options in order:
   - Local helper script (e.g., `yt-dlp --write-auto-subs` or a wrapper like `yt-transcribe`)
   - `youtube-transcript-api` Python package (fast, no-auth, may be rate-limited)
   - Whisper on downloaded audio (slow but reliable)
   - If nothing works: ask the user to paste a transcript manually
2. Copy transcript to `sources/src-YYYYMMDD-<slug>/transcript.txt`
3. Fill `meta.yaml` with `fetch_method: yt-transcript`, type: `youtube`
4. Build `conspect.md` from the transcript (cite timings where critical)
5. Continue normal pipeline from step 5 (atomize onwards)

## Style the user expects

Not a neutral rewording. Structure like an analyst briefing:

1. **What the piece actually says** — core thesis, key facts.
2. **What's real / по делу** — claims that check out.
3. **What's marketing / hype / unverified** — call it out explicitly.
4. **Your critical take** — what's missing, what's oversimplified.
5. **Practical takeaway for the user** — given what they're building.

Language: **Russian**. Tone: direct, short sentences, no fluff.

## Committing changes

University is under git (if initialized). After processing a URL, files to `git add`:
- `sources/<src-id>/` (entire folder)
- `notes/n-*.md` (new notes)
- `claims/c-*.md` (new claims)
- `syntheses/<topic>.md` (if updated)
- `graph/edges.jsonl` (appended lines)
- `INDEX.md` (updated rows)
- `queue/inbox.md` (link moved from Pending to Processed)

**Do NOT auto-commit.** Ask user first or wait for them to commit.
