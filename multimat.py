from __future__ import unicode_literals

import maya.cmds as cmds
import maya.api.OpenMaya as om2

shape = 'pSphereShape1'

sel_list = om2.MGlobal.getSelectionListByName(shape)
obj = sel_list.getDependNode(0)
dag_path = sel_list.getDagPath(0)
fn = om2.MFnDependencyNode(obj)

inst_groups = fn.findPlug('instObjGroups', False)

for i in xrange(inst_groups.numElements()):
    inst_group = inst_groups.elementByLogicalIndex(i)
    obj_groups = inst_group.child(0)

    for j in xrange(obj_groups.numElements()):
        obj_group = obj_groups.elementByLogicalIndex(j)
        
        print om2.MFnDependencyNode(obj_group.connectedTo(False, True)[0].node()).name()
        
        for k in xrange(obj_group.numChildren()):
            child = obj_group.child(k)

            if child.name().endswith('.objectGrpCompList'):
                comps = om2.MFnComponentListData(child.asMObject())

                for l in xrange(comps.length()):
                    comp = comps.get(l)
                    iter = om2.MItMeshPolygon(dag_path, comp)
                    while not iter.isDone():
                        print iter.index()
                        iter.next(iter)
                break

