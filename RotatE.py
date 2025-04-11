# Импорт библиотек
from neo4j import GraphDatabase
import pandas as pd
from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.models.predict import get_tail_prediction_df
from pykeen.evaluation import RankBasedEvaluator
import json
import time

# Подключение к Neo4j
host = 'bolt://localhost:7687'
user = 'neo4j'
password = '11111111'
driver = GraphDatabase.driver(host, auth=(user, password))

def run_query(query, params={}):
    with driver.session() as session:
        result = session.run(query, params)
        return pd.DataFrame([r.values() for r in result], columns=result.keys())

# Получение данных из Neo4j
data = run_query("""
MATCH (s)-[r]->(t)
RETURN toString(id(s)) as source, toString(id(t)) AS target, type(r) as type
""")

# Создание TriplesFactory для PyKeen
tf = TriplesFactory.from_labeled_triples(
    data[["source", "type", "target"]].values,
    create_inverse_triples=False,
    entity_to_id=None,
    relation_to_id=None,
    compact_id=False,
    filter_out_candidate_inverse_relations=True,
    metadata=None,
)

# Разделение данных на обучающую, тестовую и валидационную выборки
training, testing, validation = tf.split([.8, .1, .1])

# Обучение модели RotatE
result = pipeline(
    training=training,
    testing=testing,
    validation=validation,
    model='RotatE',
    stopper='early',
    epochs=1,
    dimensions=512,
    random_seed=420
)

# Оценка модели
start_time = time.time()  # Запускаем таймер перед оценкой

# Создаем экземпляр RankBasedEvaluator
evaluator = RankBasedEvaluator()

metrics = evaluator.evaluate(result.model, testing.mapped_triples)

# Получаем метрики
hits_1 = metrics.get_metric("hits@1")
hits_3 = metrics.get_metric("hits@3")
hits_5 = metrics.get_metric("hits@5")
hits_10 = metrics.get_metric("hits@10")
mrr = metrics.get_metric("mean_reciprocal_rank")

# Оценка времени выполнения
end_time = time.time()
evaluation_time = end_time - start_time  # Время выполнения в секундах

# Составляем словарь с результатами
results = {
    "Hits@1": hits_1 if isinstance(hits_1, (int, float)) else "N/A",
    "Hits@3": hits_3 if isinstance(hits_3, (int, float)) else "N/A",
    "Hits@5": hits_5 if isinstance(hits_5, (int, float)) else "N/A",
    "Hits@10": hits_10 if isinstance(hits_10, (int, float)) else "N/A",
    "Mean Reciprocal Rank (MRR)": mrr if isinstance(mrr, (int, float)) else "N/A",
    "Evaluation Time (seconds)": evaluation_time
}

# Путь к файлу JSON
json_file_path = 'rotate-log.json'

# Записываем результаты в JSON файл
with open(json_file_path, 'w') as json_file:
    json.dump(results, json_file, indent=4)

# Выводим результаты в консоль
print("Оценка модели:")
print(f'Hits@1: {hits_1 if isinstance(hits_1, (int, float)) else "N/A"}')
print(f'Hits@3: {hits_3 if isinstance(hits_3, (int, float)) else "N/A"}')
print(f'Hits@5: {hits_5 if isinstance(hits_5, (int, float)) else "N/A"}')
print(f'Hits@10: {hits_10 if isinstance(hits_10, (int, float)) else "N/A"}')
print(f'Mean Reciprocal Rank (MRR): {mrr if isinstance(mrr, (int, float)) else "N/A"}')
print(f'Evaluation Time (seconds): {evaluation_time:.4f}')
# Получение предсказаний для соединения L-Asparagine
compound_id = run_query("""
MATCH (s:Compound)
WHERE s.name = "L-Asparagine"
RETURN toString(id(s)) as id
""")['id'][0]

df = get_tail_prediction_df(result.model, compound_id, 'treats', triples_factory=result.training)
print(df.head(5))

# Сохранение топ-5 предсказаний обратно в Neo4j
candidate_nodes = df[df['in_training'] == False].head(5)['tail_label'].to_list()

run_query("""
MATCH (n)
WHERE id(n) = toInteger($compound_id)
UNWIND $candidates as ca
MATCH (c)
WHERE id(c) = toInteger(ca)
MERGE (n)-[:PREDICTED_TREATS]->(c)
""", {'compound_id': compound_id, 'candidates': candidate_nodes})

# Просмотр результатов
predictions = run_query("""
MATCH (c:Compound)-[:PREDICTED_TREATS]->(d:Disease)
RETURN c.name as compound, d.name as disease
""")
print(predictions)

# Поиск путей для объяснения предсказаний
paths = run_query("""
MATCH (c:Compound {name: "L-Asparagine"}),(d:Disease {name:"colon cancer"})
WITH c,d
MATCH p=AllShortestPaths((c)-[r:binds|regulates|interacts|upregulates|downregulates|associates*1..4]-(d))
RETURN [n in nodes(p) | n.name] LIMIT 25
""")
print(paths)
