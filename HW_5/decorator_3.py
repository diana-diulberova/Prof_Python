import types
import os
from decorator_2 import logger


path = 'application_operation.log'

@logger(path)
def flat_generator(list_of_lists):
    for items in list_of_lists:
        for i in items:
            yield i

@logger(path)
def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)

    object = flat_generator(list_of_lists_1)
    print(type(object))

    for i in object:
        print(i)

if __name__ == '__main__':

    if os.path.exists(path):
        os.remove(path)

    test_2()
