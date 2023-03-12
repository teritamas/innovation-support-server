# innovation-support-server

イノベーションサポートの BE です。

## API ドキュメント

API の種類や仕様に関しては下記の URL を参照

- [DAO Innovation Support](https://innovation-support-server-fae3im6i6q-an.a.run.app/docs)

## Quick Start

```sh:
poetry install
poetry run pytest .
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## その他スクリプト

### テストユーザを作成し投票

```sh:
poetry run python scripts/sample_vote.py -h
usage: sample_vote.py [-h] [--proposal_id PROPOSAL_ID] [--voter_count VOTER_COUNT]
                      [--agreement_rate AGREEMENT_RATE]

options:
  -h, --help            show this help message and exit
  --proposal_id PROPOSAL_ID
                        投票対象の提案ID
  --voter_count VOTER_COUNT
                        投票数
  --agreement_rate AGREEMENT_RATE
                        賛成の割合
```

`test_proposal_id`に賛成比率を 7 割で 200 票投票する場合は、下記のコマンドを実行する。

```sh:
poetry run python scripts/sample_vote.py --proposal_id=test_proposal_id --voter_count=200 --agreement_rate=0.7
```
