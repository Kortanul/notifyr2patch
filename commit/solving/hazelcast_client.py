import hazelcast


class HazelcastClient:
  def __init__(self, server_list):
    self.client = self._configure_client(server_list)

  def get_set(self, namespace, set_name):
    return self.client.get_set(f"{namespace}:{set_name}")

  @staticmethod
  def _configure_client(server_list):
    config = hazelcast.ClientConfig()
    print("Hazelcast Cluster name: {}".format(config.group_config.name))

    for peer in server_list:
      config.network_config.addresses.append(peer)

    client = hazelcast.HazelcastClient(config)
    print("Hazelcast Client is {}".format(client.lifecycle.state))

    return client
