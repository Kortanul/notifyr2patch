from commitsolving.hazelcast_client import HazelcastClient
from commitsolving.storage.hazelcast_storage import HazelcastStorage


class HazelcastUtils:
  @staticmethod
  def create_hazelcast_storage(server_list):
    client = HazelcastClient(server_list)
    hazelcast_storage = HazelcastStorage(client)

    return hazelcast_storage
