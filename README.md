# Scrooge – expense tracking

Telegram Bot and Web app for personal and family expense tracking

## 💻 How to launch

It requires PostgreSQL and Redis.

1) Install dependencies via poetry:

```bash
poetry install
```
2) Create and fill `.env` file from [example](.env.example)
3) Start bot:

```bash
python cmd/run_bot.py
```
4) Profit! Now you can interact with your bot.


Also you can install pre-commit for linting and type checking:
```bash
pre-commit install
```