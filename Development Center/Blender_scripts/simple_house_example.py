import bpy

"""
Example create a simple house implementation

https://www.blender.org/forum/viewtopic.php?t=25794
"""

verts = (
    (4, 2, 0),
    (4, -2, 0),
    (-4, -2, 0),
    (-4, 2, 0),
    (4, 2, 4),
    (4, -2, 4),
    (-4, -2, 4),
    (-4, 2, 4),
    (4, 0, 6),
    (-4, 0, 6),
)

faces = (
    (0, 1, 2, 3),
    (8, 9, 6, 5),
    (0, 4, 8, 5, 1),
    (1, 5, 6, 2),
    (2, 6, 9, 7, 3),
    (4, 0, 3, 7),
    (4, 7, 9, 8),
)

me = bpy.data.meshes.new("Simple House")
me.from_pydata(verts, [], faces)
me.validate()
me.update()

ob = bpy.data.objects.new("Simple House", me)
bpy.context.scene.objects.link(ob)
bpy.context.scene.update()
