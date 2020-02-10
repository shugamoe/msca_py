# Using sqlite library for direct connection

import sqlite3
conn = sqlite3.connect("class.db")

c = conn.cursor()

# Create table
# c.execute('''create table symbol_company(
#          Symbol CHAR(10) NOT NULL,
#           Company CHAR(10) NOT NULL,
#            PRIMARY KEY(Symbol,Company)
#             );''')

# Insert a row of data
c.execute("insert into symbol_company values ('AAL','American Airlines')")
c.execute("insert into symbol_company values ('UAL','United Airlines')")
c.execute("insert into symbol_company values ('LUV','Southwest Airlines')")
c.execute("insert into symbol_company values ('VA','Virgin America')")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
