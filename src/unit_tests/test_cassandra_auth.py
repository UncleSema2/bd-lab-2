import unittest
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra import Unauthorized


class TestCassandraAuth(unittest.TestCase):

    def setUp(self) -> None:
        self.host = "127.0.0.1"
        self.port = 9042
        self.username = "cassandra"
        self.keyspace = "breast_cancer"

    def test_cassandra_connection_with_correct_password(self):
        cluster = Cluster(
            [self.host],
            port=self.port,
            auth_provider=PlainTextAuthProvider(
                username=self.username,
                password="cassandra_pass",
            ),
        )
        try:
            session = cluster.connect(self.keyspace)
            result = session.execute("SELECT * FROM system.local").one()
            self.assertIsNotNone(result)
        finally:
            cluster.shutdown()

    def test_cassandra_connection_with_wrong_password_fails(self):
        cluster = Cluster(
            [self.host],
            port=self.port,
            auth_provider=PlainTextAuthProvider(
                username=self.username,
                password="wrong_password",
            ),
        )
        try:
            with self.assertRaises(Unauthorized):
                cluster.connect()
        finally:
            cluster.shutdown()
