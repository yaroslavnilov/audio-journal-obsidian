# Audio Journal to Obsidian (Whisper + Ollama)

Автоматический пайплайн для превращения нескольких голосых заметок за день в один структурированный, отредактированный файл дневника в формате **Obsidian Markdown**.

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
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME

python -m venv venv
source venv/bin/activate  # На Linux/macOS
# venv\Scripts\activate   # На Windows

pip install faster-whisper openai

```

### 3. Использование

1. Положите аудиофайлы (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`) в папку `audio_input/`.
2. Запустите скрипт:
```bash
python main.py

```


3. Готовый дневник появится в `processed_text/daily_journal.md`, а сырой транскрипт — в `processed_text/all_raw_combined.txt`.