## Comparison of RotatE and RotatE-NormMLP Results

To compare the results of the RotatE and RotatE-NormMLP models, we can present them in a table to clearly see what improvements have been achieved.

| Metric                     | RotatE  | RotatE-NormMLP | Difference |
| -------------------------- | ------- | -------------- | ---------- |
| Hits@1                     | 0.00455 | 0.00515        | +0.00060   |
| Hits@3                     | 0.00749 | 0.00859        | +0.00110   |
| Hits@5                     | 0.00929 | 0.01020        | +0.00091   |
| Hits@10                    | 0.01250 | 0.01340        | +0.00090   |
| Mean Reciprocal Rank (MRR) | 0.00894 | 0.00971        | +0.00077   |
| Evaluation Time (sec)      | 684.61  | 712.88         | -28.27 sec |

### Evaluation of Improvements:

- **Hits@1, Hits@3, Hits@5, Hits@10**: All of these metrics showed improvements in the RotatE-NormMLP model, with the largest gains in Hits@3 (+0.00110) and Hits@5 (+0.00091).
- **MRR**: The Mean Reciprocal Rank (MRR) also improved by +0.00077.
- **Evaluation Time**: The evaluation time increased by 28.27 seconds, which may be due to added regularization and normalization layers.

### Conclusion:

The RotatE-NormMLP model demonstrates improvements across all key metrics, including Hits@1, Hits@3, Hits@5, Hits@10, and Mean Reciprocal Rank (MRR). While the evaluation time has increased—likely due to additional normalization and regularization operations—the improvements in performance metrics may justify the longer runtime.

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
python RotatENormMLP.py
```
