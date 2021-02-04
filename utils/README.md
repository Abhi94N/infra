# sqlite2postgres

SQLite to Postgres migration utility base on [`pgloader`](https://pgloader.readthedocs.io/en/latest/ref/sqlite.html)

## Requirements

- `pgloader` 3.6+
- `Python` 3.6+

1. SSH into remote host

2. (Recommended) Create, activate virtualenv, and install requirements:

```bash
virtualenv -p python3 venv
source venv/bin/activate
python2 -m pip install -r requirements.txt
```

3. Install `sqlite2postgres`

```bash
git clone https://github.com/illumidesk/infra
cd infra/utils
python -m pip install .
```

4. Create `.env` file and set envioronment variable values:

```shell
cp env.example .env
```

5. Run the script

```shell
python pgloader_batch.py
```
