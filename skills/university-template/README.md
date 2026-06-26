# university-template

Переносимый шаблон Zettelkasten-базы знаний для проектов, работающих в связке с [Claude Code](https://claude.com/claude-code).

Origin: извлечён из реального проекта `meteora-bot/university/` как generic-скелет без контента.

## Что это

База знаний, управляемая по строгим правилам (METHODOLOGY.md). Работает как система: пользователь кидает ссылку → Claude обрабатывает в 10 шагов → результат попадает в структурированные папки с перекрёстными ссылками.

**Артефакты пайплайна**:
- `sources/<id>/` — первоисточники с conspect'ами
- `notes/n-<slug>.md` — атомарные заметки (одна идея = один файл)
- `claims/c-<NNNN>.md` — проверяемые утверждения с evidence
- `syntheses/syn-<topic>.md` — сводные документы
- `contradictions/contr-<NNN>.md` — зафиксированные конфликты
- `verdicts/v-<slug>.md` — итоговые решения
- `experiments/` — собственные бэктесты/симуляции
- `graph/edges.jsonl` — машиночитаемый граф связей

**Это НЕ скрипты**. Это конвенция + шаблоны. Пайплайн выполняет Claude, прочитав `METHODOLOGY.md`.

## Установка

```bash
git clone https://github.com/kkarpushin/university-template.git ~/university-template
# либо в любое удобное место
```

Дальше в любом своём проекте запускаешь `~/university-template/bootstrap.sh <project-path>` — см. раздел "Как использовать" ниже.

## Зависимости

- `bash` 4+ (стандартный на Linux/macOS)
- `python3` 3.6+ (только stdlib, ничего устанавливать не надо)
- `sed`, `find`, `cp`, `mkdir` — GNU coreutils (стандарт)
- [Claude Code](https://claude.com/claude-code) — сам шаблон работает без него, но вся ценность в связке с Claude'ом (memory-файлы, интеграция пайплайна)

## Платформы

- ✅ **Linux** (тестировалось на Ubuntu 24.04)
- ✅ **macOS** (bash 3.2 в системе — установи 5+ через brew, либо `sh` совместимый режим)
- ⚠️ **Windows** — только через WSL2 (Git Bash тоже должен работать, но не тестировалось)

## Структура этого template-репозитория

```
university-template/
├── README.md                         # этот файл — доки по шаблону
├── bootstrap.sh                      # скрипт инициализации в target-проекте
├── skeleton/                         # то что копируется в <target>/university/
│   ├── METHODOLOGY.md                # generic, с плейсхолдерами {{PROJECT_MISSION}} и {{PROJECT_NAME}}
│   ├── README.md                     # generic, с {{PROJECT_NAME}} placeholder
│   ├── TAXONOMY.md                   # пустой скелет (заполняется при инициализации)
│   ├── INDEX.md                      # пустой индекс-скелет
│   ├── _templates/                   # 7 шаблонов для всех типов артефактов
│   ├── sources/.gitkeep              # пусто
│   ├── notes/.gitkeep                # пусто
│   ├── claims/.gitkeep               # пусто
│   ├── syntheses/.gitkeep            # пусто
│   ├── contradictions/.gitkeep       # пусто
│   ├── verdicts/.gitkeep             # пусто
│   ├── experiments/.gitkeep          # пусто
│   ├── graph/edges.jsonl             # пустой файл
│   └── queue/
│       ├── inbox.md                  # пустой
│       ├── to-follow.md              # пустой
│       └── escalation.md             # пустой
└── memory-template/                  # то что попадает в Claude memory target-проекта
    ├── reference_url_summary_workflow.md   # с {{PROJECT_NAME}} и {{PROJECT_PATH}} плейсхолдерами
    └── MEMORY.md.template            # entry для MEMORY.md индекса
```

## Как использовать

### Шаг 1 — bootstrap в новый проект

```bash
# пример: инициализируем university в новом проекте ~/my-new-project
# (папка может ещё не существовать — скрипт создаст её, если родитель есть)
~/university-template/bootstrap.sh ~/my-new-project
```

Скрипт сделает:
1. Создаст `<target>` если папки ещё нет (родитель должен существовать — защита от опечаток пути)
2. Скопирует весь skeleton в `<target>/university/`
3. Заменит `{{PROJECT_NAME}}` на имя папки проекта (автоматически)
4. Создаст Claude memory file с правильными путями
5. Добавит entry в `MEMORY.md` этого memory-dir
6. **Запустит интерактивный интервью** (`interview.py`) — задаст 6 вопросов и сам заполнит плейсхолдеры

После этого Claude в новой сессии на проект автоматически увидит memory и будет направлять все URL через университет.

### Шаг 2 — ответить на 6 вопросов интервью

Bootstrap после копирования скелета запустит `python3 interview.py <target>` автоматически. Вопросы:

1. **Миссия проекта** (обязательное, одно предложение)
   — _пример: «Построить прибыльную LP-стратегию на Meteora DLMM»_

2. **Seed docs** (опционально, список)
   — существующие документы проекта, которые надо обработать как первичные внутренние источники
   — формат: `<path> — описание`, по одному на строку, пустая строка = готово

3. **IN-SCOPE темы** (список)
   — что университет принимает для обработки
   — пример: `Концентрированная ликвидность — модели IL`

4. **OUT-OF-SCOPE темы** (список)
   — что сразу отклоняем (защита от расплывания)
   — пример: `NFT / GameFi — не наш домен`

5. **Таксономия** (список листьев дерева)
   — формат: `<root>/<leaf> — описание`
   — пример: `lp-mechanics/impermanent-loss — модели IL`

6. **Пути к коду/docs** (опционально, для §14)
   — пути, с которыми университет сравнивает знания
   — пример: `apps/orchestrator/src/ — оркестратор решений`

После ответов скрипт покажет summary и попросит подтверждения (`Y/n`).

**Важно**: интервью работает только в **настоящем терминале** (TTY). Если bootstrap запущен из окружения без TTY (например, изнутри Claude Code Bash tool) — интервью автоматически skip'ается с warning'ом, и его надо запустить отдельно в терминале:

```bash
python3 ~/university-template/interview.py ~/my-new-project
```

### Альтернатива: `--no-interview`

Если хочешь заполнить вручную или скриптом позже:

```bash
~/university-template/bootstrap.sh <target> --no-interview
```

Тогда плейсхолдеры останутся как есть (с инструкциями), их нужно заменить вручную в:
- `<project>/university/METHODOLOGY.md` — §1 (Миссия), §1.1 (seed), §2 (scope), §14 (bridge paths)
- `<project>/university/TAXONOMY.md` — дерево тем
- `<project>/university/README.md` — `{{PROJECT_MISSION}}`
- `<project>/university/INDEX.md` — Pre-existing sources table

Или можно запустить интервью отдельно позже:

```bash
python3 ~/university-template/interview.py <target>
```

### Шаг 3 — первый URL

```bash
# вариант A: вручную в inbox
echo "- https://example.com/paper — какой-то paper про X" >> <project>/university/queue/inbox.md

# вариант B: просто в чате Claude
# → "обработай https://example.com/paper"
# Claude прочитает memory → увидит что URL обрабатывается через university →
# прочитает METHODOLOGY → выполнит пайплайн
```

### Опционально — git-init

Рекомендуется коммитить university как часть проекта (или отдельный submodule):

```bash
cd <project>/university/
git init && git add -A && git commit -m "university: bootstrap from template"
```

## Переключение между проектами

У тебя **несколько проектов** с университетами? Никаких конфликтов:
- Каждый университет живёт внутри своего проекта (`<project>/university/`)
- Каждый Claude memory привязан к своему `~/.claude/projects/<path-slug>/memory/` (slug = абсолютный путь проекта, где `/` → `-`)
- Когда открываешь Claude Code в проекте X — только его memory активна
- Content (sources, notes, claims) не пересекается

## Обновление template

Если ты улучшаешь METHODOLOGY.md или шаблоны **в этом template-репо**, то существующие университеты в проектах **не обновятся автоматически**. Это by design: каждый проект живёт своей жизнью.

Для обновления:
```bash
# вручную скопировать новый файл поверх
cp ~/university-template/skeleton/METHODOLOGY.md <project>/university/METHODOLOGY.md
# потом вернуть проект-специфичные правки (§1, §1.1, §2, §14)
```

Или использовать `bootstrap.sh` с `--force` (перезапишет всё — осторожно):
```bash
~/university-template/bootstrap.sh <project> --force
```

## Создание нового проекта "с нуля"

```bash
# 1. создать проект
mkdir ~/my-new-project
cd ~/my-new-project
git init

# 2. bootstrap university
~/university-template/bootstrap.sh $(pwd)

# 3. открыть Claude Code в этой папке
# cd ~/my-new-project
# claude

# → в сессии Claude автоматически подтянет memory и будет следовать правилам university
```

## История

Template извлечён из реальной работающей Zettelkasten-базы (2026, проект `meteora-bot`) как generic pattern. Всё проектное содержимое (источники, заметки, утверждения, синтезы, экспериментальный код) оставлено в исходном проекте — здесь только методология, шаблоны и пустой скелет.

## Возможные улучшения (на будущее)

- [ ] Опциональный Python/bash `graph-validator.sh` — проверка целостности `graph/edges.jsonl` (нет dangling references)
- [ ] Markdown-линтер для atomic-notes (проверка frontmatter, обязательность Links секции)
- [ ] GitHub Action: при коммите в university/ автоматически перегенерировать INDEX.md из содержимого папок
- [ ] MCP server для Claude — прямой доступ к graph без чтения jsonl

Пока всё pure markdown — можно использовать в любой Claude Code сессии без дополнительного тулинга.
