
tests = [
  'with x as (select 1 from dual) select * from x where id = 1',
  'with x as (select 1 from dual) select a, b, c from x where id = 1', 
  'with x as (select 1 from dual) select * from x where a = 1 and b = 2', 
  'with x as (select 1 from dual) select * from x where (a = 1 and b = 2)',
  'with x as (select 1 from dual) select * from x where ((a = 1 and b = 2))'
  'with x as (select 1 from dual) select * from x where (a = 1 and b = 2) or (c = 3)',
  'with x as (select * from x where ((a = 1 and b = 2))) select * from x'
]

[convert(t) for t in tests]
