# innovation-support-server

## API ドキュメント

API の種類や仕様に関しては下記の URL を参照

- [DAO Innovation Support](https://innovation-support-server-fae3im6i6q-an.a.run.app/docs)

## Quick Start

```sh:
poetry install
poetry run pytest .
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
