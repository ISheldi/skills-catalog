#!/usr/bin/env python3
"""Interactive post-bootstrap setup for a university/ skeleton.

Interviews the operator and fills in the placeholders in:
  - METHODOLOGY.md (§1 mission, §1.1 seed docs, §2 scope in/out, §14 bridge paths)
  - TAXONOMY.md (topic tree)
  - INDEX.md (Pre-existing internal sources table)
  - README.md ({{PROJECT_MISSION}} token)

Usage:
  python3 interview.py <target-project-path>

The target must already contain a `university/` directory created by bootstrap.sh.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple


# -------- I/O helpers -------------------------------------------------------

def hr():
    print("─" * 60)


def header(n: int, total: int, title: str):
    hr()
    print(f"  [{n}/{total}]  {title}")
    hr()


def ask_single(prompt: str, required: bool = True, example: str | None = None) -> str:
    """Ask a single-line question. Re-prompts if required and empty."""
    if example:
        print(f"  пример: {example}")
    while True:
        try:
            answer = input(f"> ").strip()
        except EOFError:
            print()  # newline after ^D
            sys.exit("aborted (EOF)")
        if answer or not required:
            return answer
        print("  (поле обязательное, попробуй ещё раз)")


def ask_bullets(help_text: str, example: str | None = None) -> List[str]:
    """Collect bullets, one per line. Empty line ends input. Returns list of strings
    (without leading dash). Empty list OK."""
    print(f"  {help_text}")
    if example:
        print(f"  пример строки: {example}")
    print("  (пустая строка = закончили)")
    bullets: List[str] = []
    while True:
        try:
            line = input(f"  {len(bullets)+1}> ").strip()
        except EOFError:
            print()
            break
        if not line:
            break
        # Strip leading "- " if user typed it
        if line.startswith("- "):
            line = line[2:]
        bullets.append(line)
    return bullets


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        try:
            answer = input(f"{prompt} {hint}: ").strip().lower()
        except EOFError:
            print()
            return default
        if not answer:
            return default
        if answer in ("y", "yes", "д", "да"):
            return True
        if answer in ("n", "no", "н", "нет"):
            return False
        print("  (введи y или n)")


# -------- File substitution -------------------------------------------------

def replace_section(file_path: Path, section_id: str, new_content: str) -> bool:
    """Replace content between BOOTSTRAP:PLACEHOLDER:<id> and BOOTSTRAP:END:<id> sentinels.

    Returns True if replaced, False if sentinels not found.
    """
    text = file_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf'<!-- BOOTSTRAP:PLACEHOLDER:{re.escape(section_id)} -->.*?<!-- BOOTSTRAP:END:{re.escape(section_id)} -->',
        re.DOTALL,
    )
    replacement = (
        f'<!-- BOOTSTRAP:FILLED:{section_id} -->\n'
        f'{new_content}\n'
        f'<!-- BOOTSTRAP:END:{section_id} -->'
    )
    new_text, n = pattern.subn(replacement, text)
    if n == 0:
        return False
    file_path.write_text(new_text, encoding="utf-8")
    return True


def replace_token(file_path: Path, token: str, value: str) -> int:
    """Replace all occurrences of `{{TOKEN}}` in file with value. Returns count."""
    text = file_path.read_text(encoding="utf-8")
    new_text = text.replace(token, value)
    count = text.count(token)
    if count > 0:
        file_path.write_text(new_text, encoding="utf-8")
    return count


# -------- Content builders --------------------------------------------------

def build_mission_section(mission: str) -> str:
    return (
        f'Собрать и систематизировать знания, достаточные, чтобы **{mission}**. '
        f'«Обоснованно» = каждое решение в коде/стратегии можно привязать к конкретному '
        f'атомарному утверждению (`claim`), которое привязано к конкретному первоисточнику.\n\n'
        f'База знаний не заменяет код/продукт — она его **обосновывает и проверяет**.'
    )


def build_bullet_list(items: List[str], empty_placeholder: str = "_Пока нет._") -> str:
    if not items:
        return empty_placeholder
    return "\n".join(f"- {item}" for item in items)


def build_index_seed_table(seed_docs: List[Tuple[str, str]]) -> str:
    """seed_docs is list of (path, description) tuples."""
    if not seed_docs:
        return (
            "| Path | Role | Quality | Relevance |\n"
            "|------|------|---------|-----------|\n"
            "| _(пока нет pre-existing docs)_ | — | — | — |"
        )
    lines = [
        "| Path | Role | Quality | Relevance |",
        "|------|------|---------|-----------|",
    ]
    for path, desc in seed_docs:
        lines.append(f"| [{path}]({path}) | {desc} | pending | 5 |")
    return "\n".join(lines)


def parse_seed_docs(raw: List[str]) -> List[Tuple[str, str]]:
    """Parse 'path — description' format into (path, description) tuples.
    Fallback: if no '—' separator, treat whole line as path with generic description."""
    result = []
    for line in raw:
        if "—" in line:
            path, _, desc = line.partition("—")
            result.append((path.strip(), desc.strip()))
        elif " - " in line:
            path, _, desc = line.partition(" - ")
            result.append((path.strip(), desc.strip()))
        else:
            result.append((line.strip(), "pre-existing document"))
    return result


def build_taxonomy_tree(entries: List[str]) -> str:
    """Convert taxonomy entries into a tree code block.

    Each entry is either:
      'root/'                       — root topic
      'root/leaf — description'     — leaf with description
    """
    if not entries:
        return "```\n<root-topic>/\n└── <leaf>/   — что сюда попадает\n```"

    # Group by root topic
    roots: dict[str, List[Tuple[str, str]]] = {}
    for entry in entries:
        # Handle leaf: "root/leaf — description" or "root/leaf - description"
        if "—" in entry or " - " in entry:
            sep = "—" if "—" in entry else " - "
            path_part, _, description = entry.partition(sep)
            description = description.strip()
        else:
            path_part = entry
            description = ""

        path_part = path_part.strip().rstrip("/")
        if "/" in path_part:
            root, leaf = path_part.split("/", 1)
            roots.setdefault(root, []).append((leaf, description))
        else:
            # Bare root
            roots.setdefault(path_part, [])

    # Render tree
    lines = ["```"]
    root_list = list(roots.items())
    for i, (root, leaves) in enumerate(root_list):
        lines.append(f"{root}/")
        for j, (leaf, desc) in enumerate(leaves):
            is_last = j == len(leaves) - 1
            branch = "└──" if is_last else "├──"
            if desc:
                lines.append(f"{branch} {leaf}/    — {desc}")
            else:
                lines.append(f"{branch} {leaf}/")
        if i < len(root_list) - 1:
            lines.append("")
    lines.append("```")
    return "\n".join(lines)


# -------- Main interview ----------------------------------------------------

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python3 interview.py <target-project-path>")

    target = Path(sys.argv[1]).resolve()
    uni = target / "university"
    if not uni.is_dir():
        sys.exit(f"ERROR: {uni} does not exist. Run bootstrap.sh first.")

    methodology = uni / "METHODOLOGY.md"
    taxonomy = uni / "TAXONOMY.md"
    readme = uni / "README.md"
    index = uni / "INDEX.md"

    for f in (methodology, taxonomy, readme, index):
        if not f.exists():
            sys.exit(f"ERROR: expected file missing: {f}")

    project_name = target.name

    print()
    hr()
    print(f"  University Setup Interview — project: {project_name}")
    hr()
    print(
        "\n  Отвечай на вопросы по очереди. Всё можно пропустить на пустой строке "
        "(кроме миссии). В конце файлы будут обновлены.\n"
    )

    # Q1: Mission (required)
    header(1, 6, "Миссия проекта")
    print("  Одним предложением опиши, какое знание должна обосновать эта база знаний.")
    print("  Пример 1: «Построить прибыльную LP-стратегию на Meteora DLMM»")
    print("  Пример 2: «Создать API для автоматического on-chain анализа токенов»")
    print()
    mission = ask_single("", required=True)

    # Q2: Seed docs
    print()
    header(2, 6, "Существующие документы проекта (seed)")
    print("  Есть ли уже написанные docs/research-файлы в проекте, которые надо")
    print("  обработать как первичные внутренние источники (relevance=5)?")
    print()
    seed_docs_raw = ask_bullets(
        "Одна запись на строку в формате: <путь> — описание",
        example="project-docs/architecture.md — архитектура бота",
    )
    seed_docs = parse_seed_docs(seed_docs_raw)

    # Q3: In-scope
    print()
    header(3, 6, "Темы IN-SCOPE (что обрабатываем)")
    print("  Какие темы источников бот должен принимать для обработки?")
    print()
    in_scope = ask_bullets(
        "Одна тема на строку (краткое описание).",
        example="Концентрированная ликвидность (Uniswap v3, DLMM) — модели IL",
    )

    # Q4: Out-of-scope
    print()
    header(4, 6, "Темы OUT-OF-SCOPE (что отклоняем)")
    print("  Какие темы надо сразу отсекать, чтобы скоуп не расползался?")
    print()
    out_scope = ask_bullets(
        "Одна тема на строку.",
        example="NFT / GameFi — не наш домен",
    )

    # Q5: Taxonomy
    print()
    header(5, 6, "Таксономия (дерево тем для syntheses/)")
    print("  Иерархия тем, по которым будут строиться сводные документы.")
    print("  Формат строки: <root>/<leaf> — описание")
    print("  Бросать строки по одной; каждый путь '<root>/<leaf>' создаёт лист в дереве.")
    print()
    taxonomy_entries = ask_bullets(
        "Одна строка = один лист таксономии.",
        example="lp-mechanics/impermanent-loss — модели IL и их измерение",
    )

    # Q6: Bridge paths (optional)
    print()
    header(6, 6, "Пути к коду/docs для моста (§14) — опционально")
    print("  Пути к файлам/папкам проекта, с которыми университет будет сравнивать")
    print("  свои знания (код, стратегия, decisions log). Можно пропустить.")
    print()
    bridge_paths_raw = ask_bullets(
        "Одна запись на строку: <путь> — описание",
        example="apps/orchestrator/src/ — оркестратор стратегических решений",
    )

    # ---- Summary + confirmation ----
    print()
    hr()
    print("  Готов записать?")
    hr()
    print(f"  Миссия:         {mission}")
    print(f"  Seed docs:      {len(seed_docs)} шт")
    print(f"  In-scope:       {len(in_scope)} пунктов")
    print(f"  Out-of-scope:   {len(out_scope)} пунктов")
    print(f"  Taxonomy:       {len(taxonomy_entries)} листьев")
    print(f"  Bridge paths:   {len(bridge_paths_raw)} шт")
    print()
    if not ask_yes_no("Применить?", default=True):
        print("отменено; ничего не изменено.")
        sys.exit(0)

    # ---- Apply substitutions ----
    changes: List[str] = []

    # METHODOLOGY.md §1 mission
    if replace_section(methodology, "section_mission", build_mission_section(mission)):
        changes.append(f"  ✓ METHODOLOGY.md §1 (Миссия)")

    # METHODOLOGY.md §1.1 seed docs
    seed_content = build_bullet_list(
        [f"`{p}` — {d}" for p, d in seed_docs],
        empty_placeholder="_Пока нет pre-existing документов для обработки как seed._",
    )
    if replace_section(methodology, "section_seed_docs", seed_content):
        changes.append(f"  ✓ METHODOLOGY.md §1.1 (Seed docs)")

    # METHODOLOGY.md §2 scope in
    if replace_section(methodology, "section_scope_in", build_bullet_list(in_scope)):
        changes.append(f"  ✓ METHODOLOGY.md §2 in-scope")

    # METHODOLOGY.md §2 scope out
    if replace_section(methodology, "section_scope_out", build_bullet_list(out_scope)):
        changes.append(f"  ✓ METHODOLOGY.md §2 out-of-scope")

    # METHODOLOGY.md §14 bridge paths
    bridge_bullets = [f"   - `{line.split('—', 1)[0].strip() if '—' in line else line.split(' - ', 1)[0].strip()}` — "
                      f"{line.split('—', 1)[1].strip() if '—' in line else (line.split(' - ', 1)[1].strip() if ' - ' in line else '')}"
                      for line in bridge_paths_raw]
    # Indent with 3 spaces to fit the numbered list
    if bridge_paths_raw:
        bridge_content = "\n".join(bridge_bullets)
    else:
        bridge_content = "   - _(no paths configured yet — добавь когда появятся компоненты для сравнения)_"
    if replace_section(methodology, "section_bridge_paths", bridge_content):
        changes.append(f"  ✓ METHODOLOGY.md §14 bridge paths")

    # TAXONOMY.md tree
    if replace_section(taxonomy, "section_taxonomy_tree", build_taxonomy_tree(taxonomy_entries)):
        changes.append(f"  ✓ TAXONOMY.md tree")

    # INDEX.md seed table
    if replace_section(index, "section_index_preexisting", build_index_seed_table(seed_docs)):
        changes.append(f"  ✓ INDEX.md Pre-existing seed table")

    # README.md + METHODOLOGY.md mission token substitution
    readme_replaced = replace_token(readme, "{{PROJECT_MISSION}}", mission)
    methodology_replaced = replace_token(methodology, "{{PROJECT_MISSION}}", mission)
    if readme_replaced > 0:
        changes.append(f"  ✓ README.md: заменён {{PROJECT_MISSION}} ({readme_replaced} раз)")
    if methodology_replaced > 0:
        changes.append(f"  ✓ METHODOLOGY.md: заменён {{PROJECT_MISSION}} ({methodology_replaced} раз)")

    # ---- Done ----
    print()
    hr()
    print("  Изменения применены:")
    hr()
    for c in changes:
        print(c)
    print()
    print("  Следующий шаг — открой файлы и проверь глазами:")
    print(f"    {methodology}")
    print(f"    {taxonomy}")
    print(f"    {readme}")
    print(f"    {index}")
    print()
    print("  Если всё ок — git add & commit.")
    print()


if __name__ == "__main__":
    main()
