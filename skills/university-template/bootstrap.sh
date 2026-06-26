#!/usr/bin/env bash
# university-template bootstrap
# Usage:
#   bootstrap.sh <target-project-path> [--force] [--no-interview]
#
# Copies the generic university skeleton into <target>/university/, plus
# creates a Claude Code memory entry so future sessions on that project
# automatically route every URL through the university pipeline
# (per METHODOLOGY.md).
#
# By default, runs interactive interview (interview.py) after copying to fill
# in project-specific placeholders. Use --no-interview to skip and fill manually.
#
# Example:
#   ./bootstrap.sh ~/my-new-project
#   → creates ~/my-new-project/university/
#   → creates ~/.claude/projects/<path-slug>/memory/reference_url_summary_workflow.md
#     (slug = absolute project path with '/' replaced by '-')
#   → launches interactive interview to fill placeholders
#
# License: MIT (see LICENSE)

set -euo pipefail

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKELETON_DIR="$TEMPLATE_DIR/skeleton"
MEMORY_TEMPLATE_DIR="$TEMPLATE_DIR/memory-template"
INTERVIEW_SCRIPT="$TEMPLATE_DIR/interview.py"

err() { echo "ERROR: $*" >&2; exit 1; }
warn() { echo "WARN: $*" >&2; }

[[ $# -ge 1 ]] || err "usage: $0 <target-project-path> [--force] [--no-interview]"

TARGET="$1"
FORCE=0
RUN_INTERVIEW=1
shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift;;
    --no-interview) RUN_INTERVIEW=0; shift;;
    *) err "unknown flag: $1";;
  esac
done

# Resolve TARGET to absolute path. If missing, create it (expected for fresh projects).
# Parent must exist — we don't create arbitrary path prefixes to avoid typos creating garbage.
if [[ -d "$TARGET" ]]; then
  TARGET="$(cd "$TARGET" && pwd)"
else
  PARENT_DIR="$(dirname "$TARGET")"
  BASE_NAME="$(basename "$TARGET")"
  [[ -d "$PARENT_DIR" ]] || err "parent directory does not exist: $PARENT_DIR (create it or fix the path typo)"
  ABS_PARENT="$(cd "$PARENT_DIR" && pwd)"
  TARGET="$ABS_PARENT/$BASE_NAME"
  echo ">> Target does not exist, creating: $TARGET"
  mkdir "$TARGET" || err "failed to create target: $TARGET"
fi

PROJECT_NAME="$(basename "$TARGET")"
UNIVERSITY_DIR="$TARGET/university"

# Derive Claude Code memory directory slug from absolute path:
# /home/alice/foo-bar → -home-alice-foo-bar
CLAUDE_SLUG="$(echo "$TARGET" | sed 's|/|-|g')"
CLAUDE_MEMORY_DIR="$HOME/.claude/projects/$CLAUDE_SLUG/memory"

echo "=== university-template bootstrap ==="
echo "Target project: $TARGET"
echo "Project name:   $PROJECT_NAME"
echo "University dir: $UNIVERSITY_DIR"
echo "Claude memory:  $CLAUDE_MEMORY_DIR"
echo

# Step 1: check target doesn't already have a university (unless --force)
if [[ -d "$UNIVERSITY_DIR" && $FORCE -eq 0 ]]; then
  err "$UNIVERSITY_DIR already exists. Use --force to overwrite (will clobber existing files)."
fi

# Step 2: copy skeleton
echo ">> Copying skeleton…"
mkdir -p "$UNIVERSITY_DIR"
cp -r "$SKELETON_DIR/." "$UNIVERSITY_DIR/"
echo "   done: $(find "$UNIVERSITY_DIR" -type f | wc -l) files copied"

# Step 3: substitute {{PROJECT_NAME}} in the copied university files
# (we keep {{PROJECT_MISSION}} as-is — user fills that manually, it's an intentional placeholder)
echo ">> Substituting {{PROJECT_NAME}} in skeleton…"
find "$UNIVERSITY_DIR" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.jsonl" \) -print0 |
  xargs -0 sed -i "s|{{PROJECT_NAME}}|$PROJECT_NAME|g"

# Step 4: set up Claude memory
echo ">> Setting up Claude memory at $CLAUDE_MEMORY_DIR…"
mkdir -p "$CLAUDE_MEMORY_DIR"

MEMORY_FILE="$CLAUDE_MEMORY_DIR/reference_url_summary_workflow.md"
if [[ -f "$MEMORY_FILE" && $FORCE -eq 0 ]]; then
  warn "$MEMORY_FILE exists, skipping (use --force to overwrite)"
else
  cp "$MEMORY_TEMPLATE_DIR/reference_url_summary_workflow.md" "$MEMORY_FILE"
  sed -i "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" "$MEMORY_FILE"
  sed -i "s|{{PROJECT_PATH}}|$TARGET|g" "$MEMORY_FILE"
  echo "   done: $MEMORY_FILE"
fi

# Step 5: append to MEMORY.md if exists, else create
MEMORY_INDEX="$CLAUDE_MEMORY_DIR/MEMORY.md"
ENTRY_LINE="- [URL processing → university pipeline](reference_url_summary_workflow.md) — CRITICAL. Every URL goes through $TARGET/university/ Zettelkasten, NOT chat summary. Read METHODOLOGY.md first."

if [[ -f "$MEMORY_INDEX" ]]; then
  if grep -q "reference_url_summary_workflow.md" "$MEMORY_INDEX"; then
    warn "MEMORY.md already has url-summary-workflow entry, skipping"
  else
    echo "$ENTRY_LINE" >> "$MEMORY_INDEX"
    echo "   appended entry to existing MEMORY.md"
  fi
else
  echo "$ENTRY_LINE" > "$MEMORY_INDEX"
  echo "   created new MEMORY.md"
fi

echo
echo "=== ✓ skeleton copy complete ==="
echo

# Step 6: interactive interview (unless --no-interview)
if [[ $RUN_INTERVIEW -eq 1 ]]; then
  if [[ ! -t 0 ]]; then
    warn "stdin is not a TTY — cannot run interactive interview. Skipping."
    warn "Run it manually later:  python3 $INTERVIEW_SCRIPT $TARGET"
    RUN_INTERVIEW=0
  elif ! command -v python3 >/dev/null 2>&1; then
    warn "python3 not found — cannot run interview. Skipping."
    warn "Install python3, then: python3 $INTERVIEW_SCRIPT $TARGET"
    RUN_INTERVIEW=0
  else
    echo
    echo ">> Launching interactive interview (Ctrl+C to skip)…"
    echo
    python3 "$INTERVIEW_SCRIPT" "$TARGET" || warn "Interview aborted/failed — placeholders remain. Re-run: python3 $INTERVIEW_SCRIPT $TARGET"
  fi
fi

echo
echo "=== ✓ bootstrap complete ==="
echo
if [[ $RUN_INTERVIEW -eq 0 ]]; then
  echo "Next steps (manual — interview was skipped):"
  echo
  echo "  Run interview later:  python3 $INTERVIEW_SCRIPT $TARGET"
  echo "  OR edit placeholders manually in:"
  echo "     - $UNIVERSITY_DIR/METHODOLOGY.md"
  echo "         § 1 (Миссия): replace {{PROJECT_MISSION}}"
  echo "         § 1.1 (seed): list your pre-existing docs"
  echo "         § 2 (Scope): define in-scope / out-of-scope for THIS project"
  echo "         § 14 (Bridge to product): point to your code/docs paths"
  echo "     - $UNIVERSITY_DIR/TAXONOMY.md"
  echo "         Replace example tree with actual topic hierarchy"
  echo "     - $UNIVERSITY_DIR/README.md"
  echo "         Replace {{PROJECT_MISSION}} (one-liner for the project)"
  echo "     - $UNIVERSITY_DIR/INDEX.md"
  echo "         Add Pre-existing internal sources table if you have any"
  echo
fi

echo "Verify Claude memory picked up:"
echo "   cat $MEMORY_INDEX"
echo
echo "Optional — git-init the university:"
echo "   cd $UNIVERSITY_DIR && git init && git add -A && git commit -m 'university: bootstrap from template'"
echo
echo "Drop your first URL in:"
echo "   $UNIVERSITY_DIR/queue/inbox.md"
echo "   — or just paste the URL into a Claude session on the project"
echo
