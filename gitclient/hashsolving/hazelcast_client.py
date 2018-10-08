import hazelcast


class HazelcastClient:
  def __init__(self, commit_id):
    self.client = self._configure_cluster()
    self.commit_id = commit_id

  @property
  def solution_attempt_set(self):
    return self.client.get_set(f"{self.commit_id}:solution_attempt_set")

  def _configure_cluster(self):
    config = hazelcast.ClientConfig()
    print("Cluster name: {}".format(config.group_config.name))

    config.network_config.addresses.append("127.0.0.1:5701")
    config.network_config.addresses.append("127.0.0.1:5702")

    client = hazelcast.HazelcastClient(config)
    print("Client is {}".format(client.lifecycle.state))

    return client
