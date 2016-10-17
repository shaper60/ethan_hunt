import os

import psycopg2

def create_dump():
   conn = psycopg2.connect(database='api2', user='postgres', password='', host='192.168.99.100', port='32775')

   # Open a cursor to perform database operations
   cur = conn.cursor()

   #os.remove("copy_data")
   copy_file = "/tmp/copy_data.sql"
   cur.execute("COPY (SELECT * FROM products_product WHERE created > '2016-07-20') TO '%s';" % copy_file)

   os.system('eval "$(docker-machine env default)"')
   os.system("docker cp ee544ad715b2:/tmp/copy_data.sql copy_data.sql")

   cur.close()
   conn.close()
create_dump()

