# Alpha Mini Platform: Керівництво зі створення алгоритмів (Algorithms Layer)

Цей документ допоможе вам створювати складні, інтерактивні сценарії та логіку поведінки робота у шарі **`src/alpha_mini_pkg/algorithms`**.



---

## 1. Роль та Принципи Шару Algorithms

Шар `algorithms` містить **високорівневі стратегії** (наприклад, ігри, місії, інтерактивні діалоги).

* **Принцип Чистоти:** Алгоритм не має прямого доступу до SDK або низькорівневих сервісів. Він використовує лише інструменти, надані шаром **Core**.
* **Цілісність:** Якщо ваша логіка вимагає використання циклу `while` або динамічного прослуховування, вона повинна бути реалізована тут, а не в **Core** чи **Listeners**.

### Точка Входу Алгоритму

Наразі вся складна логіка платформи активується через єдину команду **"start"**. Обробник команд делегує виконання універсальній функції:

```
# У Command Handler:
from alpha_mini_pkg.algorithms import execute_main_algorithm
# ...
await execute_main_algorithm(text_command)
```

---

## 2. Створення нового алгоритму

### Крок 1: Визначення файлу та імпортів

Створіть файл у каталозі `src/alpha_mini_pkg/algorithms/` (наприклад, `my_mission.py`). Імпортуйте лише інструменти з пакета `alpha_mini_pkg.core`.

```
# src/alpha_mini_pkg/algorithms/my_mission.py

import logging
import asyncio
import re # Для парсингу команд
from alpha_mini_pkg.core import (
    action_walk,
    action_speak,
    action_play_named,
    MoveRobotDirection,
    create_dynamic_listener # Ключовий інструмент для інтерактиву
)
from alpha_mini_pkg.utils.helpers import safe_delay

logger = logging.getLogger(__name__)

async def execute_new_mission(text: str):
    logger.info("ALGORITHM: Запуск нової місії.")
    await action_speak("Місія розпочата!")
    # ... Ваша логіка
```

### Крок 2: Інтеграція в Main Algorithm

Щоб активувати вашу нову місію, інтегруйте її в основний алгоритм, який запускається за командою "start".

```
# src/alpha_mini_pkg/algorithms/main_algorithm.py

from .my_mission import execute_new_mission

async def execute_main_algorithm(text: str):
    # Або запустіть динамічний слухач, або виконайте місію.
    
    if "mission" in text.lower():
        await execute_new_mission(text)
    else:
        # Стандартна логіка динамічного прослуховування
        # ...
```

---

## 3. Інструментарій Алгоритмів (API Toolbox)

Ваші алгоритми мають доступ до наступних високоякісних інструментів із шару **`core`**:

### А. Атомарні Дії (Actions)

Це ваш базовий набір команд для керування роботом.

| Функція | Призначення | Приклад Виклику |
| :--- | :--- | :--- |
| **`action_walk(steps, direction)`** | Переміщує робота на певну кількість кроків у заданому напрямку. | `await action_walk(5, MoveRobotDirection.FORWARD)` |
| **`action_speak(text)`** | Озвучує текст і чекає, доки робот закінчить говорити. | `await action_speak("Hello!")` |
| **`action_play_named(name)`** | Виконує попередньо задану анімаційну дію (наприклад, "Wave"). | `await action_play_named("Dance")` |
| **`MoveRobotDirection`** | **Enum** для визначення напрямку (FORWARD, BACKWARD, TURN\_LEFT, TURN\_RIGHT). | Використовуйте його як константу. |

### B. Динамічний Слухач (DynamicListener)

Це потужний інструмент для створення інтерактивних сценаріїв, де робот чекає на конкретну відповідь.

| Функція | Призначення |
| :--- | :--- |
| **`create_dynamic_listener(loop)`** | Створює новий екземпляр слухача. |
| **`listener.on_speaking(callback)`** | Реєструє **асинхронну** функцію, яка викликається при кожному розпізнаванні мови. |
| **`listener.stop_when(phrase)`** | Встановлює ключову фразу, при розпізнаванні якої цикл прослуховування зупиниться. |
| **`await listener.start()`** | Запускає цикл і блокує виконання алгоритму, доки не спрацює умова зупинки. |

### Приклад Динамічної Взаємодії (Парсинг Команд)

Ось як можна використовувати `DynamicListener` для динамічного парсингу команд (як ви просили):

```
async def execute_interactive_walk(text: str):
    loop = asyncio.get_running_loop()
    listener = create_dynamic_listener(loop)
    
    await action_speak("I am waiting for your walk command. Say 'walk [number] steps [direction]', or say 'done'.")

    # 1. Створення функції-обробника для кожної розпізнаної фрази
    async def command_parser_callback(speech_text: str):
        normalized = speech_text.lower()
        
        # Регулярний вираз для пошуку: "walk <число> steps <напрямок>"
        # (Напрямки: forward, backward, left, right)
        match = re.search(r"walk\s+(\d+)\s+steps\s+(forward|backward|left|right)", normalized)
        
        if match:
            steps = int(match.group(1))
            direction_name = match.group(2)
            
            # Перетворення рядка на константу Direction
            direction_map = {
                "forward": MoveRobotDirection.FORWARD, 
                "backward": MoveRobotDirection.BACKWARD,
                "left": MoveRobotDirection.TURN_LEFT, 
                "right": MoveRobotDirection.TURN_RIGHT
            }
            direction = direction_map.get(direction_name)

            if direction:
                await action_speak(f"Executing {steps} steps {direction_name}.")
                await action_walk(steps, direction)
            else:
                await action_speak("Sorry, I don't know that direction.")
        else:
            await action_speak(f"I heard {speech_text}, but I'm waiting for a walk command.")

    # 2. Налаштування та запуск: реєструємо обробник і умову зупинки
    listener.on_speaking(command_parser_callback).stop_when("done")

    # 3. Блокування виконання до команди "done"
    stop_phrase = await listener.start()
    
    await action_speak(f"Interactive mode finished. You said: {stop_phrase}")
    
# Щоб запустити це, ви можете інтегрувати його в execute_main_algorithm.
```

---

Сподіваюся, це керівництво допоможе вам створювати складні та захоплюючі сценарії! Дайте знати, якщо виникнуть питання щодо API.