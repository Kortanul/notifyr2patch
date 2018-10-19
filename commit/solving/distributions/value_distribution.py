import random
from operator import itemgetter

import numpy
from lazy import lazy


##
# The abstract representation of the probability distribution for a given set
# of values.
#
# Values can be thresholded, so that values above or below a certain value are
# disregarded. Values can also be scaled, so that the distribution represents
# them in coarser-grained increments
#
# For example, consider the following distribution of times:
# [0, 300, 450, 30, 10, 12, 15, 18, 900, 400, 404, 500]
#
# If min_value is 10, and max_value is 500, then the distribution is modeled
# as if the values were:
# [300, 450, 30, 10, 12, 15, 18, 400, 402, 500]
#
# If the bucket_width is 5 (e.g. 5 seconds), the distribution is scaled and
# put into buckets of the following values:
# [60, 90, 6, 2, 2, 80, 80, 100]
#
# The distribution would be:
# {2: 0.20, 3: 0.10, 4: 0.10, 6: 0.10, 60: 0.10, 80: 0.20, 90: 0.10, 100: 1.00}
#
class ValueDistribution:
  def __init__(self, values, bucket_width=1, min_value=None, max_value=None):
    self.values = values
    self.bucket_width = bucket_width

    if min_value is not None:
      self.min_value = min_value
    else:
      self.min_value = min(values)

    if max_value is not None:
      self.max_value = max_value
    else:
      self.max_value = max(values)

    if self.min_value >= self.max_value:
      raise ValueError('max_value must be greater than min_value')

  @lazy
  def distribution_values(self):
    return list(self.distribution.keys())

  @lazy
  def distribution_weights(self):
    return list(self.distribution.values())

  @lazy
  def most_frequent_value(self):
    sorted_values = \
      sorted(self.distribution.items(), key=itemgetter(1), reverse=True)

    first_value = next(iter(sorted_values), (None, None))

    return first_value[0]

  @lazy
  def distribution(self):
    scaled_values = [
      value / self.bucket_width
      for value in self.values
      if self.min_value <= value <= self.max_value
    ]

    distribution = self._calculate_distribution(scaled_values)

    return distribution

  def pick_range(self):
    start_value = self.pick_value()
    range = numpy.arange(start_value, start_value + self.bucket_width)

    return range

  def pick_value(self):
    try:
      choice = \
        random.choices(self.distribution_values, self.distribution_weights)

      choice_value = next(iter(choice), 0)

    except IndexError:
      choice_value = 0

    scaled_choice_value = choice_value * self.bucket_width

    return scaled_choice_value

  def __str__(self):
    return str(self.distribution)

  def _calculate_distribution(self, values):
    min_scaled_value = self.min_value / self.bucket_width
    max_scaled_value = self.max_value / self.bucket_width

    # Avoid divide by zero when there are no values
    if len(values) == 0:
      return {min_scaled_value: 1.0}

    histogram, bins = \
      numpy.histogram(
        values,
        bins=numpy.arange(min_scaled_value, max_scaled_value),
        density=True
      )

    distribution_map = dict(zip(bins, histogram))

    condensed_distribution = {
      offset.item(): distribution.item()
      for (offset, distribution) in distribution_map.items()
      if distribution > 0
    }

    return condensed_distribution
