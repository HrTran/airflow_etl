CREATE TABLE IF NOT EXISTS persons (
    id SERIAL PRIMARY KEY,
    t_01 int,
    t_02 int,	
    t_03 int,
    n_01 int,
    total int,
    created_on TIMESTAMP DEFAULT NOW()
);
