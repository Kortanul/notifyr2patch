from commitsolving.committimepicking.factories.probabilistic_time_picker_factory import \
  ProbabilisticTimePickerFactory
from commitsolving.committimepicking.probabilistic_incremental_time_picker \
  import ProbabilisticIncrementalTimePicker


class ProbabilisticIncrementalTimePickerFactory(ProbabilisticTimePickerFactory):
  def _create_time_picker(self, distribution):
    return ProbabilisticIncrementalTimePicker(distribution)
