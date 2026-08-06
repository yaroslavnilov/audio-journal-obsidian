# Audio Journal to Obsidian (Whisper + Ollama)

Автоматический пайплайн для превращения нескольких голосовых заметок за день в один структурированный, отредактированный файл дневника в формате **Obsidian Markdown**.

## 🛠 Технологии
* **[faster-whisper](https://github.com/SYSTRAN/faster-whisper)** — локальное распознавание аудио (Faster Whisper `medium` / CPU `int8`).
* **[Ollama](https://ollama.com/)** + **[OpenAI Python API](https://github.com/openai/openai-python)** — объединение, редактура и форматирование заметок под стиль Obsidian (`gpt-oss:120b-cloud`).

## 🚀 Быстрый старт

### 1. Требования
* Python 3.9+
* Запущенный сервер **Ollama** с загруженной моделью:
  ```bash
  ollama run gpt-oss:120b-cloud

```

### 2. Установка

Клонируйте репозиторий и установите зависимости:

```bash
git clone [https://github.com/yaroslavnilov/audio-journal-obsidian.git](https://github.com/yaroslavnilov/audio-journal-obsidian.git)
cd audio-journal-obsidian

python -m venv venv
# venv\Scripts\activate     # На Windows
# source venv/bin/activate  # На Linux/macOS

pip install -r requirements.txt

```

### 3. Использование

1. Положите аудиофайлы (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`) в папку `audio_input/`.
2. Запустите скрипт:
```bash
python main.py

```


3. Готовый дневник появится в `processed_text/daily_journal.md`, а сырой транскрипт — в `processed_text/all_raw_combined.txt`.