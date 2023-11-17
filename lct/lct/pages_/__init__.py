from collections import namedtuple

from .videos_from_archive import main as videos_from_archive
from .rtc import main as rtc
from .api import main as api
from .history import main as history
from .teach import main as teach
from .settings import main as settings


Page = namedtuple("Page", "title method")

pages: dict[str, Page] = {
    'archive': Page(title="Разпознать из архива", method=videos_from_archive),
    'rtc': Page(title="Rtc трансляции", method=rtc),
    'history': Page(title="История распознаваний", method=history),
    'teach': Page(title="Обучение", method=teach),
    'settings': Page(title="Настройки", method=settings),
    'api': Page(title="Уведомления", method=api)
}
