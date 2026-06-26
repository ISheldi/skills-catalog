#!/usr/bin/env python3
"""
Агент для адаптации сообщений при коммуникации с нарциссом
Использует базу знаний из NotebookLM
"""

import sys
import subprocess
import json
import os

# Пути к NotebookLM
NOTEBOOKLM_PATH = os.path.expanduser("~/.claude/skills/notebooklm")
RUN_SCRIPT = os.path.join(NOTEBOOKLM_PATH, "scripts", "run.py")

# Запрещённые фразы - триггеры нарциссической ярости
FORBIDDEN_PHRASES = [
    "я тебя понимаю",
    "решай сам",
    "мне всё равно",
    "извинись",
    "признай вину",
    "давай честно",
    "скажи правду",
    "ты сделал мне больно",
    "ты нарцисс",
    "ты обидел",
    "почему ты",
    "ты всегда",
    "ты никогда",
]

# Паттерны оправданий
JUSTIFICATION_PATTERNS = [
    "потому что",
    "из-за того что",
    "так как",
    "ведь ты",
]

def query_notebooklm(question):
    """Запрос к базе знаний NotebookLM"""
    try:
        result = subprocess.run(
            [
                "python3",
                RUN_SCRIPT,
                "ask_question.py",
                "--question",
                question
            ],
            cwd=NOTEBOOKLM_PATH,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            # Извлекаем ответ из вывода
            output = result.stdout
            if "Question:" in output and "=" * 50 in output:
                parts = output.split("=" * 50)
                if len(parts) >= 3:
                    answer = parts[2].strip()
                    # Убираем "EXTREMELY IMPORTANT" блок
                    if "EXTREMELY IMPORTANT:" in answer:
                        answer = answer.split("EXTREMELY IMPORTANT:")[0].strip()
                    return answer

        return None
    except Exception as e:
        print(f"⚠️ Ошибка запроса к NotebookLM: {e}", file=sys.stderr)
        return None

def detect_dangerous_elements(text):
    """Обнаружение опасных элементов в тексте"""
    dangers = []
    text_lower = text.lower()

    # Проверка на запрещённые фразы
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text_lower:
            dangers.append({
                "type": "forbidden_phrase",
                "phrase": phrase,
                "reason": get_phrase_danger_reason(phrase)
            })

    # Проверка на оправдания
    for pattern in JUSTIFICATION_PATTERNS:
        if pattern in text_lower:
            dangers.append({
                "type": "justification",
                "phrase": pattern,
                "reason": "Оправдания воспринимаются как слабость и провоцируют дальнейшее давление"
            })

    # Проверка на эмоциональные слова
    emotional_words = ["обида", "боль", "больно", "устал", "устала", "страдаю", "плачу"]
    for word in emotional_words:
        if word in text_lower:
            dangers.append({
                "type": "emotion",
                "phrase": word,
                "reason": "Демонстрация эмоций даёт нарциссу карту твоих уязвимостей для будущих манипуляций"
            })

    return dangers

def get_phrase_danger_reason(phrase):
    """Получить причину опасности фразы"""
    reasons = {
        "я тебя понимаю": "Воспринимается как 'Я вижу тебя насквозь, я знаю кто ты' → паника разоблачения",
        "решай сам": "Воспринимается как 'Ты мне не важен, ты пустое место' → нарциссическая ярость",
        "мне всё равно": "Безразличие хуже ненависти для нарцисса → сильнейший триггер",
        "извинись": "Извинение = признание дефектности → активация глубинного стыда",
        "признай вину": "Признание ошибки = 'я плохой и никчемный' → защитная агрессия",
        "давай честно": "Воспринимается как 'Ты лжец, я тебя поймал' → ярость или перекладывание вины",
        "скажи правду": "Требование правды загоняет в угол → защитная агрессия",
        "ты сделал мне больно": "Даёт карту уязвимостей для будущих ударов",
        "ты нарцисс": "Бесполезно и опасно → обвинит тебя или обесценит источник",
    }
    return reasons.get(phrase, "Провоцирует нарциссическую ярость или даёт материал для манипуляций")

def determine_situation_type(goal, text):
    """Определить тип ситуации"""
    goal_lower = goal.lower() if goal else ""
    text_lower = text.lower() if text else ""

    if any(word in goal_lower for word in ["попросить", "прошу", "хочу чтобы", "извинение"]):
        return "request"
    elif any(word in goal_lower for word in ["отказать", "отказ", "сказать нет", "не хочу"]):
        return "refusal"
    elif any(word in goal_lower for word in ["договориться", "согласовать", "обсудить", "договорённость"]):
        return "negotiation"
    elif any(word in text_lower for word in ["кричишь", "злишься", "агрессия", "конфликт", "скандал"]):
        return "conflict"
    else:
        return "unknown"

def get_situation_patterns(situation_type):
    """Получить паттерны для типа ситуации"""
    patterns = {
        "request": {
            "name": "Просьба",
            "structure": "[Комплимент грандиозности] + [Просьба как возможность проявить исключительность]",
            "examples": [
                "Ты всегда такой сильный и уверенный. Думаю, такой классный человек, как ты, может признать, что что-то идёт не так",
                "Помоги мне понять, что для тебя здесь важно?",
                "Мне сложно чувствовать себя комфортно, когда..."
            ]
        },
        "refusal": {
            "name": "Отказ",
            "structure": "[Твёрдое 'нет'] + [Констатация факта без эмоций]",
            "examples": [
                "Нет, я не буду этого делать сейчас. Я занята своими делами",
                "Мне нужно время, чтобы всё обдумать",
                "Не сейчас"
            ]
        },
        "negotiation": {
            "name": "Переговоры",
            "structure": "[Факт из прошлого] + [Факт настоящего] + [Предложение обсудить]",
            "examples": [
                "Вчера мы договорились о пункте А, сегодня он нарушен. Давай зафиксируем это",
                "У меня не сходятся тут кое-какие моменты, возможно, я что-то упускаю. Как бы ты мог дополнить картину?",
                "Я готов к любому твоему решению. Выбор за тобой"
            ]
        },
        "conflict": {
            "name": "Конфликт",
            "structure": "[Называние манипуляции] + [Спокойное констатирование] + [Аналитический вопрос]",
            "examples": [
                "Я вижу, что ты делаешь. Я вижу, что ты пытаешься заставить меня чувствовать вину",
                "Интересно, почему ты выбрал именно такие слова?",
                "Я вижу, что ты сделал, и мне неважно, почему"
            ]
        }
    }
    return patterns.get(situation_type, patterns["request"])

def generate_output(goal, context, draft, dangers, situation_type, adapted_message, explanation, alternatives=None):
    """Генерация форматированного вывода"""
    output = []

    output.append("## 🎯 ТВОЯ ЦЕЛЬ")
    output.append(goal)
    output.append("")

    if dangers:
        output.append("## ⚠️ ЧТО ОПАСНО В ТВОЁМ ЧЕРНОВИКЕ")
        for danger in dangers:
            phrase = danger.get("phrase", "")
            reason = danger.get("reason", "")
            output.append(f"- **«{phrase}»** → {reason}")
        output.append("")

    output.append("## ✅ АДАПТИРОВАННОЕ СООБЩЕНИЕ")
    output.append("")
    output.append(adapted_message)
    output.append("")

    output.append("## 🧠 ПОЧЕМУ ЭТО РАБОТАЕТ")
    output.append(explanation)
    output.append("")

    if alternatives:
        output.append("## 📋 АЛЬТЕРНАТИВНЫЕ ВАРИАНТЫ")
        output.append("")
        for i, alt in enumerate(alternatives, 1):
            output.append(f"**Вариант {i}:**")
            output.append(alt)
            output.append("")

    # Паттерны для ситуации
    pattern = get_situation_patterns(situation_type)
    output.append(f"## 📝 ПАТТЕРН ДЛЯ СИТУАЦИИ: {pattern['name']}")
    output.append(f"**Структура:** {pattern['structure']}")
    output.append("")
    output.append("**Примеры:**")
    for example in pattern['examples']:
        output.append(f"- {example}")
    output.append("")

    return "\n".join(output)

def main():
    """Основная функция"""
    # Чтение входных данных
    if len(sys.argv) < 2:
        print("Использование: narcissist_agent.py '<JSON с данными>'")
        print("Или: narcissist_agent.py --interactive")
        sys.exit(1)

    if sys.argv[1] == "--interactive":
        # Интерактивный режим
        print("🎯 Агент коммуникации с нарциссом")
        print("")
        goal = input("Цель (что хочешь добиться): ").strip()
        context = input("Контекст (опционально, Enter для пропуска): ").strip()
        draft = input("Твой черновик сообщения: ").strip()
    else:
        # JSON режим
        try:
            data = json.loads(sys.argv[1])
            goal = data.get("goal", "")
            context = data.get("context", "")
            draft = data.get("draft", "")
        except json.JSONDecodeError:
            # Простой текстовый режим
            goal = "Адаптировать сообщение для общения с нарциссом"
            context = ""
            draft = sys.argv[1]

    if not draft:
        print("❌ Ошибка: не указан черновик сообщения")
        sys.exit(1)

    print("\n🔍 Анализирую сообщение...\n")

    # Анализ опасных элементов
    dangers = detect_dangerous_elements(draft)

    # Определение типа ситуации
    situation_type = determine_situation_type(goal, draft)

    # Простая адаптация (без запроса к NotebookLM для стандартных случаев)
    # Для демонстрации создадим базовую адаптацию
    adapted_message = adapt_message_simple(draft, situation_type, dangers)
    explanation = generate_explanation(situation_type, dangers)

    # Генерация вывода
    result = generate_output(
        goal=goal,
        context=context,
        draft=draft,
        dangers=dangers,
        situation_type=situation_type,
        adapted_message=adapted_message,
        explanation=explanation
    )

    print(result)

def adapt_message_simple(draft, situation_type, dangers):
    """Простая адаптация сообщения на основе базовых правил"""
    # Это упрощённая версия. В реальности здесь можно использовать более сложную логику
    # или запросы к NotebookLM для нестандартных ситуаций

    if situation_type == "refusal":
        return "Нет, я не буду этого делать сейчас. Я занят(а) своими делами, а к этому вернусь позже."

    elif situation_type == "request":
        return "Помоги мне понять, что для тебя здесь важно? Было бы здорово, если бы мы могли найти решение."

    elif situation_type == "negotiation":
        return "Давай зафиксируем факты: мы договорились о X, сейчас ситуация Y. Как бы ты мог дополнить эту картину?"

    elif situation_type == "conflict":
        return "Я вижу, что происходит. Интересно, что конкретно вызвало у тебя такую реакцию?"

    else:
        return "Мне нужно время, чтобы всё обдумать. Давай вернёмся к этому разговору позже."

def generate_explanation(situation_type, dangers):
    """Генерация объяснения почему это работает"""
    explanations = {
        "refusal": "- Твёрдое 'нет' без оправданий\n- Констатация факта вместо эмоций\n- Нет критики его поведения",
        "request": "- Мягкий вход через вопрос\n- Нет прямого требования\n- Иллюзия совместного решения",
        "negotiation": "- Язык фактов, не эмоций\n- Фиксация нарушения договорённости\n- Возврат к конкретике",
        "conflict": "- Называние манипуляции лишает её силы\n- Спокойствие разрывает его шаблон\n- Аналитический вопрос вместо эмоций"
    }

    base = explanations.get(situation_type, "- Сохранение спокойствия\n- Отсутствие эмоциональной реакции")

    if dangers:
        base += "\n- Убраны все триггеры нарциссической ярости"

    return base

if __name__ == "__main__":
    main()
