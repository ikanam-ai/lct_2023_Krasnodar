from collections import namedtuple

from .videos_from_archive import main as videos_from_archive
from .rtc import main as rtc
from .api import main as api
from .history import main as history
from .teach import main as teach


Page = namedtuple("Page", "title method")

pages: dict[str, Page] = {
    'archive': Page(title="Разпознать из архива", method=videos_from_archive),
    'rtc': Page(title="Rtc трансляции", method=rtc),
    'history': Page(title="История распознаваний", method=history),
    'fakes': Page(title="Обучение", method=teach),
    'api': Page(title="Уведомления", method=api)
}
