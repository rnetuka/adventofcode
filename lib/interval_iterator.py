class IntervalIterator:

    def __init__(self, interval):
        if interval.is_empty():
            self.range = None
        else:
            self.range = iter(range(interval.start, interval.end + 1))

    def __next__(self):
        if self.range is None:
            raise StopIteration()

        return next(self.range)
