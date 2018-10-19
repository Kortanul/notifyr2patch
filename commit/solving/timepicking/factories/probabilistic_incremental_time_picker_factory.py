from commit.solving.timepicking.factories.probabilistic_time_picker_factory import \
  ProbabilisticTimePickerFactory
from commit.solving.timepicking.probabilistic_incremental_time_picker import \
  ProbabilisticIncrementalTimePicker


class ProbabilisticIncrementalTimePickerFactory(ProbabilisticTimePickerFactory):
  def _create_time_picker(self, distribution):
    return ProbabilisticIncrementalTimePicker(distribution)
