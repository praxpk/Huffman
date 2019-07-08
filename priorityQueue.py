class priorityQueue:
    __slots__ = 'queue', 'head'

    def __init__(self):
        self.queue = []
        self.queue.append(-1)

    def insert_node(self, aNode):
        self.queue.append(aNode)
        self.heapify()

    def _heapify(self, start):
        smallest = start
        left = 2 * start
        right = (2 * start) + 1
        if left < len(self.queue) and self.queue[left].get_value() < self.queue[smallest].get_value():
            smallest = left
        if right < len(self.queue) and self.queue[right].get_value() < self.queue[smallest].get_value():
            smallest = right
        if smallest != start:
            self.swap(smallest, start)

    def heapify(self):
        for i in range((len(self.queue) // 2) + 1, 0, -1):
            self._heapify(i)

    def extract_min(self):
        if len(self.queue) > 1:
            minimum = self.queue.pop(1)
            self.heapify()
            return minimum
        else:
            return "End of queue"

    def get_size(self):
        return len(self.queue)-1


    def swap(self, a, b):
        temp = self.queue[a]
        self.queue[a] = self.queue[b]
        self.queue[b] = temp

    def __str__(self):
        str1 = "\n".join(str(self.queue[i]) for i in range(1, len(self.queue)))
        return str1
