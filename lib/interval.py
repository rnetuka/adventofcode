class Interval:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def empty():
        return Interval(None, None)

    @staticmethod
    def infinite():
        return Interval(float('-inf'), float('inf'))

    def is_empty(self):
        return self.start is None and self.end is None

    def intersect(self, other):
        if self.is_empty() or other.is_empty():
            return Interval.empty()
        if other.end < self.start or other.start > self.end:
            return Interval.empty()
        i = max(self.start, other.start)
        j = min(self.end, other.end)
        return Interval(i, j)

    def __repr__(self):
        if self.is_empty():
            return '()'
        return '<' + str(self.start) + ', ' + str(self.end) + '>'

    def __bool__(self):
        return not self.is_empty()

    def __contains__(self, value):
        if isinstance(value, Interval):
            return value.start >= self.start and value.end <= self.end
        return self.start <= value <= self.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __len__(self):
        return self.end - self.start + 1

    def __lt__(self, other):
        if self == other:
            return False
        if self.start < other.start:
            return True
        else:
            return self.end < other.end
