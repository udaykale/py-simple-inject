import inspect


class Inject:
    registry = []

    def __init__(self, function):
        function_name = function.__name__
        self.function = function
        if function_name != '__init__':
            raise "Cannot add @Inject on methods other than __init__"
        module_name = function.__module__
        class_name = function.__qualname__
        class_name = class_name.replace(".__init__", "")
        init_args = self.__init_args(function)

        Inject.registry.append((module_name, class_name, init_args[1:]))

    class Empty(object):
        pass

    def __call__(self, __object_graph, class_name, cls, init_arg_objs):
        obj = Inject.Empty()
        obj.__class__ = cls
        self.function(obj, *init_arg_objs)
        __object_graph[class_name] = obj

    def __init_args(self, cls):
        return list(inspect.signature(cls).parameters)
