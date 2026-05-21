[![Django CI/CD Pipeline](https://github.com/Artem4ik32/books/actions/workflows/django.yml/badge.svg)](https://github.com/Artem4ik32/books/actions/workflows/django.yml)
![Code Coverage](https://img.shields.io/badge/coverage-85%25-green)
# 📚 My Library - Django Bookstore Project

Це навчальний проєкт онлайн-книгарні, розроблений на фреймворку **Django**. Проєкт реалізує сучасні підходи до веб-розробки, включаючи асинхронність, міжнародну локалізацію та повне тестування.

## 🚀 Основні функції
* **Асинхронні Views**: Обробка замовлень та додавання в кошик без блокування сервера.
* **Інтернаціоналізація (i18n)**: Підтримка української та англійської мов.
* **Інтеграція зі Stripe**: Безпечна оплата замовлень через зовнішній сервіс.
* **Система тестування**: Покриття коду тестами (unit та integration) понад 90%.

## 🛠 Технології
- **Python 3.12**
- **Django 6.0**
- **Pytest-django** (тестування)
- **Factory-boy** (генерація тестових даних)
- **SQLite** (база даних)

## 🤖 AI Usage (Завдання з AI)
Цей проєкт було вдосконалено за допомогою штучного інтелекту.

### Використані інструменти:
* **Gemini AI** — для проведення Code Review, генерації тестів та написання документації.

### Що було зроблено через AI:
1. **Code Review**: Проведено аналіз трьох складних асинхронних views. Отримано та впроваджено поради щодо безпечного використання асинхронності в Django. (Деталі в `AI_REVIEW.md`).
2. **Генерація тестів**: AI згенерував unit-тести для моделей `Book` та `Order`, що допомогло досягти високого показника Coverage.
3. **Документація**: Всі views отримали автоматично згенеровані docstrings.
4. **Оптимізація**: Виправлення помилок асинхронного контексту в тестах.

### Промпти ( приклади з `AI_PROMPTS.md`):
- *"Review my Django async view for order creation and suggest improvements."*
- *"Generate pytest models for Book and Order models using factory-boy."*

## 🧪 Тестування та Coverage
Для запуску тестів використовуйте команду:
```bash
pytest