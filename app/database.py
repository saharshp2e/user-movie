from cassandra.cluster import Cluster

class CassandraDB:
    def __init__(self, cassandra_hosts, keyspace):
        self.cluster = Cluster(cassandra_hosts)
        self.session = self.cluster.connect(keyspace)

    def close(self):
        self.cluster.shutdown()

    def execute_query(self, query, params):
        return self.session.execute(query, params)
