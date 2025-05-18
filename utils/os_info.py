def parse_os_release(path="/etc/os-release") -> dict:
    info = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                val = val.strip().strip('"').strip("'")  # Убираем кавычки
                info[key] = val
    except FileNotFoundError:
        print(f"{path} не найден")
    return info

def parse_hostname(path="/etc/hostname") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.readline()
