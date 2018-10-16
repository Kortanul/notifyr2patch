from dateutil import tz
from lazy import lazy

from commitsolving.distributions.value_distribution import ValueDistribution

MIN_TIMEZONE_OFFSET = -43200
MAX_TIMEZONE_OFFSET = 43200


class AuthorTimezoneDistribution:
  def __init__(self, git_client, author_name):
    self.commits = self._get_commits(git_client, author_name)

  @lazy
  def distribution(self):
    author_timezone_offsets = [
      self._west_of_utc_to_tzoffset(commit.author_tz_offset)
      for commit in self.commits
    ]

    committer_timezone_offsets = [
      self._west_of_utc_to_tzoffset(commit.committer_tz_offset)
      for commit in self.commits
    ]

    all_offsets = author_timezone_offsets + committer_timezone_offsets

    # Bucket GMT-12 and GMT+12 into 1 second blocks (86,400 blocks total)
    distribution = \
      ValueDistribution(
        all_offsets,
        1,
        MIN_TIMEZONE_OFFSET,
        MAX_TIMEZONE_OFFSET
      )

    return distribution

  def pick_timezone_offset(self):
    offset_value = self.distribution.pick_value()

    return tz.tzoffset(None, offset_value)

  def __str__(self):
    return str(self.distribution)

  def _get_commits(self, git_client, author_name):
    return git_client.get_commits_by_author(author_name)

  @staticmethod
  def _west_of_utc_to_tzoffset(value):
    # Seconds WEST of UTC is opposite direction from TZ offset
    #
    # See:
    # https://stackoverflow.com/questions/11984618/why-does-python-return-a-negative-timezone-value
    return -value
