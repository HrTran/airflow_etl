CREATE TABLE IF NOT EXISTS Persons (
    id SERIAL PRIMARY KEY,
    t_01 int,
    t_02 int,	
    t_03 int,
    n_01 int,
    created_on TIMESTAMP DEFAULT NOW()
);

WITH numbers AS (
  SELECT 100 + cast((999 - 100) * random() as int) as t_01,
  	100 + cast((999 - 100) * random() as int) as t_02,
  	100 + cast((999 - 100) * random() as int) as t_03,
  	100 + cast((999 - 100) * random() as int) as n_01
  FROM generate_series(1, 5000)
)
insert into Persons (t_01, t_02, t_03, n_01)
SELECT *
FROM numbers;

