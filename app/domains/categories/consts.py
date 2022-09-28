from collections import namedtuple

DefaultCategory = namedtuple('DefaultCategory', ['name', 'is_income', 'is_outcome'])

DEFAULT_CATEGORIES = (
    DefaultCategory('🏠 Жилье', is_income=False, is_outcome=True),
    DefaultCategory('🛒 Продукты и быт', is_income=False, is_outcome=True),
    DefaultCategory('🚘 Транспорт', is_income=False, is_outcome=True),
    DefaultCategory('👖 Одежда, обувь, аксессуары', is_income=False, is_outcome=True),
    DefaultCategory('📚 Образование', is_income=False, is_outcome=True),
    DefaultCategory('🎪 Развлечения', is_income=False, is_outcome=True),
    DefaultCategory('🧑‍🍳 Кафе и рестораны', is_income=False, is_outcome=True),
    DefaultCategory('💻 Сервисы и подписки', is_income=False, is_outcome=True),
    DefaultCategory('🎁 Подарки', is_income=False, is_outcome=True),
    DefaultCategory('🧴 Красота и здоровье', is_income=False, is_outcome=True),
    DefaultCategory('🏦 Кредиты', is_income=False, is_outcome=True),
    DefaultCategory('📦 Прочее', is_income=False, is_outcome=True),
)
