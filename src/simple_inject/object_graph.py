import sys
from copy import copy
from functools import reduce

from . import Inject


class ObjectGraph:
    def __init__(self, root_objects):
        self.__object_graph = copy(root_objects)

        registry = []

        for (module_name, class_name, init_args) in Inject.registry:
            clazz = ObjectGraph.str_to_class(module_name, class_name)
            registry.append((clazz, init_args))

        self.__var_name_to_class = {each: (each, []) for each in list(root_objects.keys())}

        for cls, init_args in registry:
            class_name = self.__class_to_var_name(cls)
            self.__var_name_to_class[class_name] = (cls, init_args)

        for cls, init_args in registry:
            self.__create_class_object(cls, init_args)

    @staticmethod
    def str_to_class(module_name, classname):
        return getattr(sys.modules[module_name], classname)

    def __create_class_object(self, cls, init_args):
        class_name = self.__class_to_var_name(cls)
        if class_name in self.__object_graph:
            return self.__object_graph[class_name]

        init_arg_objs = []
        for init_arg in init_args:
            clazz, new_init_args = self.__var_name_to_class[init_arg]
            init_arg_obj = self.__create_class_object(clazz, new_init_args)
            init_arg_objs.append(init_arg_obj)

        cls(self.__object_graph, class_name, cls, init_arg_objs)
        return self.__object_graph[class_name]

    def provide(self, cls):
        var_name = self.__class_to_var_name(cls)
        return self.__object_graph.get(var_name, None)

    @staticmethod
    def __class_to_var_name(cls):
        if isinstance(cls, str):
            return cls
        return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, cls.__name__).lower()
