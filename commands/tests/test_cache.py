from commands.utils.cache import LocalCache


class HashableObject:
    def __init__(self, valuable: str, invaluable: str):
        self.valuable = valuable
        self.invaluable = invaluable

    @property
    def cache_hash(self) -> str:
        return self.valuable


def test_function_will_be_called_once():
    scope = dict(calls_counter=0)
    return_value = 'string'

    @LocalCache('test_function_will_be_called_once')
    def func() -> str:
        scope['calls_counter'] += 1
        return return_value

    assert func() == return_value
    assert func() == return_value
    assert scope['calls_counter'] == 1


def test_cache_hash_property():
    scope = dict(calls_count=0)

    @LocalCache('test_cache_hash_property')
    def func(input_value: HashableObject) -> str:
        scope['calls_count'] += 1
        return input_value.valuable

    ho_1 = HashableObject('valuable_1', 'invaluable_1')
    assert func(ho_1) == ho_1.valuable
    assert scope['calls_count'] == 1

    ho_2 = HashableObject(ho_1.valuable, 'invaluable_2')
    assert func(ho_2) == ho_1.valuable
    assert scope['calls_count'] == 1

    ho_3 = HashableObject('valuable_2', ho_1.invaluable)
    assert func(ho_3) == ho_3.valuable
    assert scope['calls_count'] == 2
