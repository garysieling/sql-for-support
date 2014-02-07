import sqlparse
from sqlparse import sql
from itertools import groupby
import ctypes

def clean(arr):
  stripped = [x.strip() for x in arr]
  return [x for x in stripped if not '(' + x + ')' in stripped]

def get_clauses(tokens):
  found = []
  for token in tokens:    
    if (token.is_group() and type(token) is sql.Parenthesis):
      found.append(token.to_unicode())
      found.extend(get_clauses(token.tokens))
    elif (token.is_group()):
      found.append(token.to_unicode())

  return found

def generate_case(token, index):
  return '(case when (' + token + ') then 1 else 0 end) as a' + str(index)

def replace_select(tokens, toSelect):
  foundSelect = False
  foundFrom = False
  addedSelect = False

  resultSql = ''
  for token in tokens:
    if token.value.lower() == 'from':
      foundFrom = True

    if not foundSelect or foundFrom:
      resultSql = resultSql + token.to_unicode()
    else:
      if not addedSelect:
        resultSql = resultSql + ' ' + toSelect + ' '
        addedSelect = True

    if token.value.lower() == 'select':
      foundSelect = True

  return resultSql

def remove_where(stmt):
  return [x for x in stmt.flatten() \
     if not x.within(sql.Where)]

def get_where(stmt):
  results = [x for x in stmt.tokens \
     if type(x) is sql.Where]

  if len(results) > 0:
    return results[0]
  else: 
    return None

def convert(sql):
  stmt = sqlparse.parse(sql)[0]

  noWhere = remove_where(stmt)
  where = get_where(stmt)
 
  toSelectColumns = '*'

  if where <> None:
    clauses = clean(get_clauses(where.tokens))

    toSelectColumns = \
      [generate_case(x, i) \
        for (i, x) in enumerate(clauses)]

  toSelect = ', '.join(toSelectColumns)

  return replace_select(noWhere, toSelect)
