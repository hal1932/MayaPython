# coding: utf-8
import maya.cmds as cmds
import maya.api.OpenMaya as om2


class Attribute(object):

    def __init__(self, plug):
        self.__plug = plug

    def cmds_get(self):
        name = self.__plug.partialName(includeNodeName=True, useFullAttributePath=True)
        return cmds.getAttr(name)


class Node(object):

    @property
    def name(self): return self.__name

    @property
    def mobject(self): return self.__mobject

    @property
    def mfn(self): return self.__mfn

    def __init__(self, name):
        self.__name = name
        self.__mobject = om2.MGlobal.getSelectionListByName(name).getDependNode(0)
        self.__mfn = om2.MFnDependencyNode(self.mobject)

    def __getattr__(self, item):
        return self.get_attribute(item)

    def get_attribute(self, name):
        plug = self.mfn.findPlug(name, False)
        return Attribute(plug)


if __name__ == '__main__':
    node_name = cmds.polyCube()
    node = Node(node_name)

    import timeit
    n = 30

    print 'findPlug: {}'.format(timeit.timeit(lambda: node.get_attribute('tx').cmds_get(), number=n))
    print 'getattr : {}'.format(timeit.timeit(lambda: node.tx.cmds_get(), number=n))
