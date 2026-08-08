import os
from datetime import datetime
from faster_whisper import WhisperModel
from openai import OpenAI

# ==================== НАСТРОЙКИ ====================
INPUT_FOLDER = "./audio_input" 
OUTPUT_FOLDER = "./processed_text"
SUPPORTED_FORMATS = (".mp3", ".wav", ".m4a", ".flac", ".ogg")

# Настройки Whisper
WHISPER_MODEL_SIZE = "medium" 
DEVICE = "cpu" 
COMPUTE_TYPE = "int8" 

# Настройки LLM (через Ollama)
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b") # Дефолтная популярная модель

SYSTEM_PROMPT = """Роль: Ты — профессиональный редактор и корректор текстов. 
Задача: Тебе передан массив из нескольких сырых голосовых заметок за день. Твоя цель — объединить их в один ЕДИНЫЙ цельный текст/дневниковую запись за день, разбив её на логические главы (например: ### Часть 1. Название, ### Часть 2. Название и т.д.).

Придерживайся следующих правил при редактировании:

1. Структура и логика:
- Объедини хронологически все заметки в один текст.
- Каждую новую аудиозапись или крупную смысловую тему выделяй подзаголовком вида "### Часть N. [Краткое вовлекающее название]".
- Разделяй текст на удобные, читаемые абзацы.
- Убирай логические тупики, повторы слов и заикания из сырой речи.

2. Грамотность и синтаксис:
- Исправляй все орфографические, пунктуационные и грамматические ошибки.
- Перестраивай слишком длинные или запутанные предложения в понятные и плавные.

3. Стиль и тональность:
- Сохраняй разговорный, живой, авторский стиль повествования.
- Оставляй авторские метафоры, сленг ("очистить буфер эмоций", "выгрузить оперативку").
- Пиши от первого лица.

Формат ответа: Выдай сразу готовый, красиво размеченный Obsidian Markdown файл с заголовками частей и вики-ссылками ([[Имя]], [[Тема]]) в ключевых местах. Без лишних предисловий и вводных фраз."""

# ===================================================

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

llm_client = OpenAI(base_url=OLLAMA_API_URL, api_key="ollama")

def transcribe_audio(model, file_path):
    """Распознавание одного аудиофайла с использованием уже загруженной модели"""
    print(f"\n[1/2] Распознавание аудио: {os.path.basename(file_path)}...")
    segments, info = model.transcribe(file_path, beam_size=5, language="ru")

    print(f"Обнаружен язык: {info.language} с точностью {info.language_probability:.2f}")

    text_segments = []
    for segment in segments:
        text_segments.append(segment.text)
        print(f"[{segment.start:.1f}s -> {segment.end:.1f}s]: {segment.text}")

    return " ".join(text_segments)

def process_combined_text_with_llm(full_raw_text):
    """Отправка ВСЕГО объединенного текста в LLM за один раз"""
    print("\n[ИИ] Начинаю общую сборку и редактирование всех заметок за день...")
    try:
        response = llm_client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Вот сырые аудиозаметки за весь день:\n\n{full_raw_text}"}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при обращении к LLM: {e}")
        return None

def main():
    audio_files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(SUPPORTED_FORMATS)])

    if not audio_files:
        print(f"В папке '{INPUT_FOLDER}' не найдено поддерживаемых аудиофайлов.")
        return

    print(f"Найдено файлов для сборки: {len(audio_files)}")

    # 1. Загружаем модель Whisper ОДИН РАЗ
    print(f"\n[Инициализация] Загрузка модели Whisper ({WHISPER_MODEL_SIZE})...")
    whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

    combined_raw_texts = []

    # 2. Транскрибируем все файлы
    for i, file_name in enumerate(audio_files, 1):
        input_path = os.path.join(INPUT_FOLDER, file_name)
        try:
            raw_text = transcribe_audio(whisper_model, input_path)
            file_entry = f"--- Заметка №{i} (Файл: {file_name}) ---\n{raw_text}"
            combined_raw_texts.append(file_entry)
        except Exception as e:
            print(f"Ошибка при распознавании файла {file_name}: {e}")
            continue

    if not combined_raw_texts:
        print("Не удалось расшифровать ни один файл.")
        return

    full_raw_payload = "\n\n".join(combined_raw_texts)

    # Генерация имени файла с текущей датой
    today_date = datetime.now().strftime("%Y-%m-%d")
    raw_output_file = os.path.join(OUTPUT_FOLDER, f"{today_date}_raw_combined.txt")
    final_output_file = os.path.join(OUTPUT_FOLDER, f"{today_date}_daily_journal.md")

    # Сохраняем сырой сборник
    with open(raw_output_file, "w", encoding="utf-8") as f:
        f.write(full_raw_payload)

    # 3. Отправляем в LLM
    final_result = process_combined_text_with_llm(full_raw_payload)

    if final_result:
        with open(final_output_file, "w", encoding="utf-8") as f:
            f.write(final_result)

        print(f"\n Успешно! Единый дневник за день сформирован:")
        print(f"-> {final_output_file}")

if __name__ == "__main__":
    main()
