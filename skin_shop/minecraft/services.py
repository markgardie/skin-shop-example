import logging
from django.conf import settings

from .rcon import RCONClient
from cart.models import Order, OrderItem

logger = logging.getLogger(__name__)


def _get_rcon_client() -> RCONClient:
    cfg = settings.MINECRAFT_RCON
    return RCONClient(
        host=cfg["HOST"],
        port=cfg["PORT"],
        password=cfg["PASSWORD"],
    )


def apply_skin(username: str, skin_url: str) -> bool:
    """
    Застосувати один скін гравцю.
    Повертає True якщо успішно, False якщо помилка.
    """
    try:
        with _get_rcon_client() as rcon:
            rcon.send_command(f"sr set {username} {skin_url}")
            logger.info(f"Скін застосовано: {username} → {skin_url}")
            return True
    except ConnectionRefusedError:
        logger.error("RCON: невірний пароль")
        return False
    except (ConnectionError, OSError) as e:
        logger.error(f"RCON: сервер недоступний — {e}")
        return False
    except Exception as e:
        logger.exception(f"RCON: невідома помилка — {e}")
        return False


def apply_skins_for_order(order: Order) -> None:
    """
    Застосувати всі скіни із замовлення.
    Оновлює статус кожного OrderItem і самого Order.
    """
    user = order.user

    if not user.minecraft_nickname:
        logger.warning(f"Користувач {user.email} не має minecraft_nickname — скіни не застосовано")
        order.status = Order.Status.FAILED
        order.save()
        return

    for item in order.order_items.select_related("skin").all():
        skin_url = item.skin.file.url
        success = apply_skin(
            username=user.minecraft_nickname,
            skin_url=skin_url,
        )
        item.status = OrderItem.Status.APPLIED if success else OrderItem.Status.FAILED
        item.save()

    order.update_status()