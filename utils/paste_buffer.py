import pyperclip
import subprocess

def copy_to_clipboard(text: str):
    """добавление текста в буфер обмена"""
    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException:
        try:
            subprocess.run(['wl-copy'], input=text.encode(), check=True)
        except Exception as e:
            raise RuntimeError("Не удалось скопировать текст в буфер обмена") from e

def paste_from_clipboard() -> str:
    """удаление текста из буфера обмена"""
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        try:
            result = subprocess.run(['wl-paste'], capture_output=True, check=True)
            return result.stdout.decode()
        except Exception as e:
            raise RuntimeError("Не удалось прочитать текст из буфера обмена") from e
