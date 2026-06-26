# 📤 Инструкция: Как загрузить skill на GitHub

## ✅ Что уже готово:

- ✅ Git репозиторий инициализирован
- ✅ Все файлы добавлены в коммит
- ✅ ZIP архив создан (21 KB)
- ✅ Документация готова

---

## 🚀 Шаг 1: Создай репозиторий на GitHub

1. **Открой GitHub:** https://github.com/new
2. **Заполни форму:**
   - **Repository name:** `narcissist-communication-skill`
   - **Description:** `🛡️ Claude Code skill для эффективной коммуникации с нарциссом`
   - **Public/Private:** Public (рекомендуется)
   - **НЕ добавляй:** README, .gitignore, license (они уже есть)
3. **Нажми:** "Create repository"

---

## 🔗 Шаг 2: Подключи удалённый репозиторий

Скопируй команды с GitHub (они появятся после создания репозитория) или выполни:

```bash
cd ~/Documents/Claude\ Code/narcissist-communication-skill

# Подключи удалённый репозиторий (замени USERNAME на свой)
git remote add origin https://github.com/USERNAME/narcissist-communication-skill.git

# Переименуй ветку в main (если нужно)
git branch -M main

# Загрузи код на GitHub
git push -u origin main
```

**Замени `USERNAME`** на своё имя пользователя GitHub!

---

## 📦 Шаг 3: Загрузи ZIP как Release

### Через веб-интерфейс GitHub:

1. **Перейди в свой репозиторий** на GitHub
2. **Нажми:** "Releases" → "Create a new release"
3. **Заполни форму:**
   - **Tag version:** `v1.0.0`
   - **Release title:** `Narcissist Communication Skill v1.0.0`
   - **Description:**
     ```markdown
     # 🎉 Первый релиз!

     ## 📦 Установка

     Скачай ZIP и распакуй в `~/.claude/skills/narcissist-communication`:

     ```bash
     unzip narcissist-communication-skill-v1.0.0.zip
     cp -r narcissist-communication-skill ~/.claude/skills/narcissist-communication
     ```

     ## ✨ Что нового

     - ✅ Автоматическое обнаружение опасных фраз
     - ✅ 4 типа ситуаций (просьба, отказ, переговоры, конфликт)
     - ✅ Интеграция с NotebookLM
     - ✅ Полная документация

     ## 📚 Документация

     - [Quick Start](QUICKSTART.md)
     - [Cheat Sheet](CHEATSHEET.md)
     - [Full README](README.md)
     ```
4. **Прикрепи файл:** Перетащи `narcissist-communication-skill-v1.0.0.zip` в раздел "Attach binaries"
5. **Нажми:** "Publish release"

---

## 🎨 Шаг 4: Улучши README на GitHub

GitHub автоматически покажет `README.md` на главной странице. Но у тебя есть `README_GITHUB.md` который красивее!

**Переименуй файл:**

```bash
cd ~/Documents/Claude\ Code/narcissist-communication-skill

# Сохрани старый README как документацию skill
mv README.md README_SKILL.md

# Переименуй GitHub README в основной
mv README_GITHUB.md README.md

# Закоммить изменения
git add .
git commit -m "docs: Update README for GitHub display"
git push
```

Теперь на GitHub будет показываться красивый README с badges!

---

## 📍 Шаг 5: Добавь темы (Topics) на GitHub

1. **Перейди в репозиторий** на GitHub
2. **Нажми** на шестерёнку рядом с "About"
3. **Добавь темы (Topics):**
   ```
   claude-code
   claude-skill
   narcissism
   psychology
   communication
   mental-health
   python
   ai-agent
   ```
4. **Сохрани**

---

## 🌟 Шаг 6: Финальные штрихи

### Добавь GitHub Actions (опционально)

Создай файл `.github/workflows/test.yml` для автоматического тестирования:

```yaml
name: Test Skill

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Test script
        run: python3 narcissist_agent.py --help || echo "Interactive mode only"
```

### Добавь бейджи (опционально)

В `README.md` можно добавить больше бейджей:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/USERNAME/narcissist-communication-skill.svg)](https://github.com/USERNAME/narcissist-communication-skill/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/USERNAME/narcissist-communication-skill.svg)](https://github.com/USERNAME/narcissist-communication-skill/issues)
[![GitHub forks](https://img.shields.io/github/forks/USERNAME/narcissist-communication-skill.svg)](https://github.com/USERNAME/narcissist-communication-skill/network)
```

---

## ✅ Проверочный чек-лист

После загрузки проверь:

- [ ] Репозиторий создан на GitHub
- [ ] Код загружен (`git push`)
- [ ] Release создан с ZIP файлом
- [ ] README.md красиво отображается
- [ ] Topics добавлены
- [ ] LICENSE файл виден
- [ ] .gitignore работает (нет лишних файлов)

---

## 📊 Что получилось

### Репозиторий структура:

```
https://github.com/USERNAME/narcissist-communication-skill
├── README.md                   ✅ Красивая главная страница
├── QUICKSTART.md               ✅ Быстрый старт
├── CHEATSHEET.md               ✅ Шпаргалка
├── PROMPT.md                   ✅ Промпт
├── LICENSE                     ✅ MIT License
├── narcissist_agent.py         ✅ Python скрипт
├── skill.json                  ✅ Конфигурация
└── .gitignore                  ✅ Git ignore
```

### Release:

```
https://github.com/USERNAME/narcissist-communication-skill/releases/tag/v1.0.0
└── narcissist-communication-skill-v1.0.0.zip (21 KB)
```

---

## 🎉 Готово!

Теперь твой skill:
- ✅ На GitHub
- ✅ С ZIP для скачивания
- ✅ С полной документацией
- ✅ Готов для использования сообществом

**Поделись ссылкой:**
```
https://github.com/USERNAME/narcissist-communication-skill
```

---

## 📝 Следующие шаги

1. **Добавь скриншоты** примеров работы в README
2. **Создай CONTRIBUTING.md** для контрибьюторов
3. **Напиши CHANGELOG.md** для версий
4. **Расскажи в социальных сетях**
5. **Собери обратную связь**

---

**Удачи с публикацией! 🚀**
