# 🎮 Тестовий Minecraft сервер для Skin Shop

## Структура файлів

```
minecraft-server/
├── docker-compose.yml          ← головний файл
├── skin_service.py             ← підключаєш до Django
├── plugins/
│   └── SkinsRestorer/
│       └── config.yml
└── data/                       ← створюється автоматично
```

---

## 🚀 Запуск (крок за кроком)

### 1. Встанови Docker
```bash
# Ubuntu/Debian
sudo apt install docker.io docker-compose-v2

# Mac — завантаж Docker Desktop з docker.com
# Windows — Docker Desktop + WSL2
```

### 2. Запусти сервер
```bash
cd minecraft-server
docker compose up -d
```

### 3. Стеж за логами (перший запуск ~2-3 хвилини)
```bash
docker compose logs -f minecraft
```
Чекай поки побачиш:
```
[Server thread/INFO]: Done (XX.XXXs)! For help, enter "help"
```

### 4. Перевір що RCON працює
```bash
# Підключись до консолі сервера
docker compose exec minecraft rcon-cli

# У консолі введи:
list
# Повинно відповісти: "There are 0 of a max of 10 players online"
exit
```

### 5. Протестуй skin_service.py
```bash
# Встанови залежності (нічого зайвого — тільки стандартна бібліотека Python!)
python skin_service.py
```

---

## 🔌 Підключення до Django

### settings.py
```python
# Додай налаштування RCON
MINECRAFT_RCON = {
    "HOST": "localhost",
    "PORT": 25575,
    "PASSWORD": "skinshop_rcon_pass",
}
```

### views.py — приклад після покупки
```python
from .skin_service import SkinService

def purchase_complete(request, skin_id):
    skin = Skin.objects.get(id=skin_id)
    username = request.user.minecraft_username  # або як у тебе зберігається
    
    service = SkinService()
    result = service.apply_skin_to_online_player(
        username=username,
        skin_url=skin.file.url  # або абсолютний URL до файлу
    )
    
    if result["success"]:
        messages.success(request, "Скін успішно застосовано!")
    else:
        messages.error(request, f"Помилка: {result['error']}")
    
    return redirect("profile")
```

### HTMX endpoint
```python
# urls.py
path("apply-skin/<int:skin_id>/", views.apply_skin_htmx, name="apply-skin"),

# views.py
def apply_skin_htmx(request, skin_id):
    # ... логіка застосування ...
    return HttpResponse(
        '<div class="alert alert-success">✅ Скін застосовано!</div>'
    )
```

---

## 🛠️ Корисні команди

```bash
# Зупинити сервер
docker compose down

# Перезапустити
docker compose restart minecraft

# Зайти в консоль Minecraft
docker compose exec minecraft rcon-cli

# Подивитись логи
docker compose logs --tail=50 minecraft

# Встановити скін вручну через консоль (для тестів)
# У rcon-cli:
sr set PlayerName https://example.com/skin.png
```

---

## 🧪 Тестування без Minecraft клієнта

Можна перевірити всю інтеграцію без входу в гру:

```bash
# 1. Запусти сервер
docker compose up -d

# 2. Зачекай ~2 хвилини

# 3. Запусти тест
python skin_service.py

# Побачиш відповідь від сервера — інтеграція працює!
```

---

## ❓ Типові проблеми

**`Connection refused` на порті 25575**
→ Сервер ще не запустився. Зачекай і повтори.

**`Wrong RCON password`**
→ Перевір що `RCON_PASSWORD` в `docker-compose.yml` і `skin_service.py` однакові.

**SkinsRestorer не встановився**
→ Перевір логи: `docker compose logs minecraft | grep -i skin`
→ Можна встановити вручну: завантаж .jar з https://github.com/SkinsRestorer/SkinsRestorerX/releases і поклади в `./plugins/`

**`ONLINE_MODE: FALSE` — навіщо?**
→ Для тестів не потрібен ліцензійний Minecraft. У продакшні встанови `TRUE`.