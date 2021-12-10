create_schema = ('''
    CREATE SCHEMA IF NOT EXISTS petl3;
''')

create_table = ('''
    CREATE TABLE IF NOT EXISTS petl3.viable_counties(
        geo_id int,
        state text,
        county text,
        sales_vector int);
''')

insert_data = ('''
    INSERT INTO petl3.viable_counties
    VALUES(%s,%s,%s,%s);
''')