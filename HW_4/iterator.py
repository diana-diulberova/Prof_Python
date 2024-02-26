class FlatIterator:

    def __init__(self, list_of_list):
        self.list = list_of_list
        self.index = 0
        self.new_list = []
        for items in self.list:
            self.new_list += items

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.new_list):
            raise StopIteration
        items = self.new_list[self.index]
        self.index += 1
        return items


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    # object = FlatIterator(list_of_lists_1)
    # print(type(object))

    # for i in object:
    #     print(i)

if __name__ == '__main__':
    test_1()
