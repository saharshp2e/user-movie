1. create a virtual env:
    conda create venv

2. Install requirements:
    pip install -r requirements.txt

3. Install & Create a keyspace in cassandra with any name,  I have used keyspace 'user_services':
    CREATE KEYSPACE user_services WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

4. Run python generator/create_table.py to create a table inside your keyspace

5. Run python generator/write_asset.py to populate the table with random data

6. Run python run.py to start the application.