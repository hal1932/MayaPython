# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import re


SOURCE_SCENE_PATH = os.path.join(os.path.dirname(__file__), '..', 'testdata', 'test.ma')
DEST_SCENE_PATH = os.path.join(os.path.dirname(__file__), '..', 'testdata', 'test_1.ma')

VISIBILITY = {
    'polymeshes': 1,
    'lights': 1,
    'textures': 1,
    'fluids': 1,
    'pluginShapes': 1,
    'nurbsCurve': 1,
    'particleInstancers': 1,
    'nCloths': 1,
}

REMOVAL = {
    'displayLayer': True,
    'animCurve': True,
    'renderLayer': True,
    'animLayer': True,
}

UNREMOVABLE_NODE_NAMES = ['defaultLayer', 'defaultRenderLayer', 'BaseAnimation']


lines = []
with open(SOURCE_SCENE_PATH, 'r') as f:
    lines = f.readlines()

for i in xrange(len(lines)):
    line = lines[i]

    if line == 'createNode script -n "uiConfigurationScriptNode";\n':
        break

ui_config_commands = []
for i in xrange(i, len(lines)):
    line = lines[i]
    if line.startswith('createNode'):
        break

    for key, value in VISIBILITY.items():
        if value == 1:
            source = 0
            dest = 1
        else:
            source = 1
            dest = 0
        lines[i] = lines[i].replace('{} {}'.format(key, source), '{} {}'.format(key, dest))


create_node_lines = {k: 'createNode {}'.format(k) for k, v in REMOVAL.items() if v}
create_node_regs = {k: re.compile('createNode {} -n "(?P<name>.+?)"'.format(k)) for k, v in REMOVAL.items() if v}

removed_node_names = []
for i in xrange(len(lines)):
    line = lines[i]
    for key, create_node in create_node_lines.items():
        if not line.startswith(create_node):
            continue

        m = create_node_regs[key].match(line)
        if not m:
            continue
        node_name = m.group('name')

        if node_name in UNREMOVABLE_NODE_NAMES:
            continue

        removed_node_names.append(m.group('name'))

        lines[i] = ''

        while True:
            i += 1
            line = lines[i]
            if not line.startswith('\t'):
                break
            lines[i] = ''

for removed_node_name in removed_node_names:
    target_line = '"{}.'.format(removed_node_name)
    for i in xrange(len(lines)):
        if target_line in lines[i]:
            lines[i] = ''


print(removed_node_names)

with open(DEST_SCENE_PATH, 'w') as f:
    f.writelines(lines)
