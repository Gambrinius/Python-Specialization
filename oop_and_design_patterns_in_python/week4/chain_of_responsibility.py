class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, type_):
        self.type = type_


class EventSet:
    def __init__(self, value):
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == int:
            return obj.integer_field
        elif isinstance(event, EventSet) and isinstance(event.value, int):
            obj.integer_field = event.value
            return obj.integer_field
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == float:
            return obj.float_field
        elif isinstance(event, EventSet) and isinstance(event.value, float):
            obj.float_field = event.value
            return obj.float_field
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == str:
            return obj.string_field
        elif isinstance(event, EventSet) and isinstance(event.value, str):
            obj.string_field = event.value
            return obj.string_field
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)


chain = IntHandler(FloatHandler(StrHandler(NullHandler())))


if __name__ == "__main__":
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"

    # test 1
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    assert chain.handle(obj, EventGet(int)) == 42
    assert chain.handle(obj, EventGet(float)) == 3.14
    assert chain.handle(obj, EventGet(str)) == 'some text'

    # test 2
    chain.handle(obj, EventSet(100))
    assert chain.handle(obj, EventGet(int)) == 100

    # test 3
    chain.handle(obj, EventSet(0.5))
    assert chain.handle(obj, EventGet(float)) == 0.5

    # test 4
    chain.handle(obj, EventSet('new text'))
    assert chain.handle(obj, EventGet(str)) == 'new text'

    print("All tests passed!")
