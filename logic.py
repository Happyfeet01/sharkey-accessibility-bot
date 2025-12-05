def find_images_without_alt(note: dict) -> list:
    images = note.get("files", [])
    return [img for img in images if not img.get("description")]

def is_valid_note(note: dict, bot_user_id: str) -> bool:
    if note.get("renote") or note.get("reply"):
        return False
    if note.get("cw") or note.get("visibility") != "public":
        return False
    if not note.get("files"):
        return False
    if note["userId"] == bot_user_id:
        return False
    return True

def build_reminder_text() -> str:
    return "Hallo! Es scheint, dass einige Bilder in deinem Post keine Beschreibungen haben. Könntest du bitte Alt-Text hinzufügen, um die Barrierefreiheit zu verbessern? Danke!"

def build_auto_description_text(descriptions: list) -> str:
    return "Hier sind einige Beschreibungen für die Bilder:\n" + "\n".join(descriptions)