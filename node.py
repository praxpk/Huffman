class node:
    __slots__ = 'left', 'right', 'value', 'character'

    def __init__(self, character, value):
        self.character = character
        self.value = value
        self.left = None
        self.right = None

    def set_left(self, node_left):
        self.left = node_left

    def set_right(self, node_right):
        self.right = node_right

    def get_value(self):
        return self.value

    def get_character(self):
        return self.character

    def __str__(self):
        string1 = "Character -> " + str(self.character) + " | Freq -> " + str(self.value)
        return string1

    def get_left(self):
        if self.left is not None:
            return self.left

    def get_right(self):
        if self.right is not None:
            return self.right


