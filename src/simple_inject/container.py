from src.simple_inject.object_graph import ObjectGraph


class Container:
    __object_graph = None

    def __init__(self, root_objects):
        Container.__object_graph = ObjectGraph(root_objects)

    @staticmethod
    def get_object_graph():
        if not Container.__object_graph:
            raise Exception("Container was not Initialized")

        return Container.__object_graph
