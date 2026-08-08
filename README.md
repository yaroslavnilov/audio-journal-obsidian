# Audio Journal to Obsidian (Whisper + Ollama)

> 🌐 *[Читать на русском языке](README_RU.md)*

An automated, **100% local and privacy-first** pipeline that turns multiple raw daily voice notes into a single structured, edited, and beautifully formatted daily journal entry in **Obsidian Markdown**.

---

## ✨ Features

* **🔒 100% Local & Private:** Your personal daily thoughts and audio files never leave your machine.
* **🎙️ Fast Local Speech-to-Text:** Powered by `faster-whisper` (`medium` / CPU `int8`) for lightweight transcription.
* **🧠 Smart AI Editing:** Uses a local LLM via `Ollama` to remove stutters, fix grammar, group notes chronologically into thematic chapters, and inject native `[[wikilinks]]`.
* **📅 Date-Based Journaling:** Automatically creates clean daily files formatted as `YYYY-MM-DD_daily_journal.md` without overwriting previous entries.
* **📝 Raw Transcript Preservation:** Saves an unedited compiled transcript (`YYYY-MM-DD_raw_combined.txt`) for debugging and reference.

---

## 🛠 Tech Stack

* **[faster-whisper](https://github.com/SYSTRAN/faster-whisper)** — Fast local audio transcription engine.
* **[Ollama](https://ollama.com/)** + **[OpenAI Python SDK](https://github.com/openai/openai-python)** — Local LLM integration for formatting and editing.

---

## 🚀 Quick Start

### 1. Prerequisites

* **Python 3.9+**
* A running **Ollama** instance with your preferred model installed (e.g., `qwen2.5:14b`, `llama3.1`, etc.):
  ```bash
  ollama run qwen2.5:14b
  ```

### 2. Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/yaroslavnilov/audio-journal-obsidian.git
cd audio-journal-obsidian

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Usage

1. Drop your voice notes (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`) into the `audio_input/` folder.
2. Run the processing script:
   ```bash
   python main.py
   ```
3. Your finished daily entry will appear in `processed_text/YYYY-MM-DD_daily_journal.md`.

---

## 🤝 Contributing

Contributions, feature requests, and issue reports are very welcome! 

Feel free to check the [Issues](https://github.com/yaroslavnilov/audio-journal-obsidian/issues) page if you want to contribute — look for tasks tagged with `good first issue`.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
