# AI Code Review Report

## 1. Async Order Creation View
**Original Code:**
Синхронна версія `create_order`, яка блокувала потік під час відправки пошти та запитів до БД.

**AI Recommendation:**
- Використати `async def` для неблокуючої обробки запитів.
- Замінити стандартні методи ORM на асинхронні аналоги (`acreate`).
- Винести відправку Email в окремий потік через `asyncio.to_thread` або імітувати асинхронність, щоб не затримувати відповідь користувачу.

**Final Code:**
(Вже реалізовано у вашому `views.py` з використанням `async def create_order`).

---

## 2. Stripe Checkout Session
**Original Code:**
Прямий виклик `stripe.checkout.Session.create`, який міг зупинити весь сервер на час очікування відповіді від API Stripe.

**AI Recommendation:**
- Огорнути зовнішній API виклик у `loop.run_in_executor`, оскільки бібліотека Stripe офіційно синхронна. Це дозволить Django обробляти інші запити, поки чекаємо на Stripe.

**Final Code:**
(Реалізовано у `views.py` через `run_in_executor`).

---

## 3. Book List Pagination
**Original Code:**
Стандартний `ListView`.

**AI Recommendation:**
- Оскільки Django ORM асинхронний лише частково, для складних запитів зі зв'язками (Select Related) рекомендується використовувати `sync_to_async` для стабільності.

**Final Code:**
(Оптимізовано у `views.py`).