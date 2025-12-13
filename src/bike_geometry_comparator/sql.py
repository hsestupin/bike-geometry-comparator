query_one_model_sql = """
WITH cte AS (SELECT * from 'data/canyon/endurace/2025/data.csv'),
unpivoted AS (UNPIVOT cte ON COLUMNS (* EXCLUDE ('size'))),
transposed AS (PIVOT unpivoted ON size USING sum(value) GROUP BY name)
SELECT name as param, * EXCLUDE (name) FROM transposed"""


set_preserve_insertion_order_sql = "SET preserve_insertion_order = true;"

query_sql = """
WITH cte AS (SELECT * from 'data/canyon/endurace/2025/geometry.csv'),
unpivoted AS (UNPIVOT cte ON COLUMNS (* EXCLUDE ('size'))),
transposed AS (
PIVOT unpivoted
ON size
IN (SELECT size from 'data/canyon/endurace/2025/geometry.csv')
USING first(value) GROUP BY name
)
SELECT --name,
       *-- EXCLUDE (param)
FROM transposed"""
