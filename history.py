# cli/history.py
import json
import os
from datetime import datetime
from pathlib import Path

HISTORY_DIR = Path.home() / ".kodeka" / "history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

class ConversationHistory:
    def __init__(self, session_name: str = "default"):
        self.session_name = session_name
        self.filepath = HISTORY_DIR / f"{session_name}.json"
        self.messages = self._load()

    def _load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def add_user_message(self, content: str):
        self.messages.append({
            "role": "user",
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.save()

    def add_assistant_message(self, content: str):
        self.messages.append({
            "role": "assistant",
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.save()

    def get_recent_history(self, max_messages: int = 12):
        return self.messages[-max_messages:]

    def clear(self):
        self.messages = []
        self.save()
