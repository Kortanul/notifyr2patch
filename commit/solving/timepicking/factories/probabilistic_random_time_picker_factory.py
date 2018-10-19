from commit.solving.timepicking.factories.probabilistic_time_picker_factory import \
  ProbabilisticTimePickerFactory
from commit.solving.timepicking.probabilistic_random_time_picker import \
  ProbabilisticRandomTimePicker


class ProbabilisticRandomTimePickerFactory(ProbabilisticTimePickerFactory):
  def _create_time_picker(self, distribution):
    return ProbabilisticRandomTimePicker(distribution)
