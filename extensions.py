import psycopg2
import config

def connect_to_database():

  params = {
    'host': config.env['host'],
    'database': config.env['db'],
    'user': config.env['user'],
    'password': config.env['password']
  }
 
  # connect to the PostgreSQL server
  db = psycopg2.connect(**params)
  return db
