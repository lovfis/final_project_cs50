import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="nor_state_stats",
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'),
        port="5432"
        )

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS nor_incomes;')
cur.execute('CREATE TABLE nor_incomes (id SERIAL,'
            'main_entry TEXT NOT NULL,'
            'year INTEGER NOT NULL,'
            'amount_in_mill INTEGER NOT NULL);'
            )

def fill_database(filename):
    file = open(filename, mode="r", encoding="ISO-8859-1")

    for count, line in enumerate(file):
        if count > 0:
            line = line.strip("\n")
            line = line.replace("A. ", "")
            line = line.split(";")
            post = line[0]
            post = post.replace('"', '')
            post = post.strip()
            year = line[1]
            year = year.replace('"', '')
            year = int(year)
            amount = int(line[2])
            #print(post, year, amount)

            # Populate database table nor_incomes
            postgres_insert_query = """INSERT INTO nor_incomes (main_entry, year, amount_in_mill) VALUES (%s, %s, %s)"""
            record_to_insert = (post, year, amount)
            cur.execute(postgres_insert_query, record_to_insert)

    file.close()

fill_database("norwegian_state_incomes.txt")

conn.commit()

cur.close()
conn.close()