## Setup Instructions

### 1. Setup Neo4j Database

- Download and install Neo4j: https://neo4j.com/download/
- Upload dump:
  - Laptop (CPU):
    - add dump file `db-mini.dump`
    - create new DBMS from a dump (version: 4.3.0)
    - name/pass: `hit`/`11111111`
  - desktop (powerful graphics cards - GPU) :
    - add dump file `db-full.dump`
    - create new DBMS from a dump (version: 5.11.0)
    - name/pass: `hit`/`11111111`
- Start the Neo4j Database

### 2. Install

- Install `pyenv`

```bush
brew install pyenv
```

- Install Python 3.8.16

```bush
pyenv install 3.8.16
```

- Set Local Python Version

```bush
pyenv local 3.8.16
```

- Create Virtual Environment

```bush
python3.8 -m venv .venv
```

- Activate Environment

```bush
source .venv/bin/activate
```

- Install Dependencies

> If you need to install deprecated `sklearn` packages, allow it with the following environment variable:

```bush
export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True pip install -r requirements.txt
```

### 3. Configure Neo4j Credentials

In your project, open the file:

**`RotatE.py`** and **RotatENormMLP.py**

Find this section:

```ts
host = "bolt://localhost:7687";
user = "neo4j";
password = "11111111";
driver = GraphDatabase.driver(host, (auth = (user, password)));
```

Replace `"11111111"` with your actual Neo4j password.

### 4. Start

To start algorithms, run:

```bash
python RotatE.py
```

```bash
RotatENormMLP.py
```
