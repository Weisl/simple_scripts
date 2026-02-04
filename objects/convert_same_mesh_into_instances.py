
import bpy
import math

# === Configuration ===
TOLERANCE = 1e-5                 # positional tolerance used when building signatures
COMPARE_IN_WORLD_SPACE = False   # set True to compare vertex positions in world space

# If you want to compare the evaluated mesh (with modifiers applied),
# set this to True (requires depsgraph and is a bit more expensive).
COMPARE_EVALUATED_MESH = False

# === Helpers ===

def get_vertex_coords(obj, world=False, evaluated=False):
    """Return a list of Vector coordinates for the object's mesh vertices.
    world=False -> object local coordinates (default, like original script)
    evaluated=True -> uses evaluated mesh (with modifiers); requires depsgraph
    """
    if evaluated:
        # Build evaluated mesh with modifiers
        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        coords = [v.co.copy() for v in mesh.vertices]
        # Clean up evaluated mesh reference
        eval_obj.to_mesh_clear()
    else:
        mesh = obj.data
        coords = [v.co.copy() for v in mesh.vertices]

    if world:
        mat = obj.matrix_world
        coords = [mat @ c for c in coords]

    return coords


def decimals_from_tolerance(tol: float) -> int:
    """Map tolerance to a rounding precision (number of decimals)."""
    # e.g. 1e-5 -> 5 decimals
    if tol <= 0:
        return 6
    return max(0, int(round(-math.log10(tol))))


def vertex_signature(obj, tol=TOLERANCE, world=COMPARE_IN_WORLD_SPACE, evaluated=COMPARE_EVALUATED_MESH):
    """Build a signature for an object based on its vertex positions.
    - Rounds coordinates to 'decimals' derived from tolerance.
    - Sorts them to be robust against vertex ordering.
    - Returns a tuple suitable as a dict key.
    """
    coords = get_vertex_coords(obj, world=world, evaluated=evaluated)
    decimals = decimals_from_tolerance(tol)

    # Round and sort
    rounded = sorted((round(c.x, decimals), round(c.y, decimals), round(c.z, decimals)) for c in coords)
    return tuple(rounded)


def group_objects_by_signature(objs):
    """Group mesh objects by their vertex-position signature."""
    sig_map = {}
    obj_to_sig = {}

    for obj in objs:
        if obj.type != 'MESH':
            continue
        sig = vertex_signature(obj)
        obj_to_sig[obj] = sig
        sig_map.setdefault(sig, []).append(obj)

    return sig_map, obj_to_sig


# === Main ===

def make_instances_from_selection():
    # Sources: selected mesh objects
    selected = [o for o in bpy.context.selected_objects if o.type == 'MESH']
    if not selected:
        print("Select one or more mesh objects first.")
        return

    # Targets: all mesh objects in the scene
    all_mesh_objs = [o for o in bpy.data.objects if o.type == 'MESH']

    # Build groups once (fast & avoids O(N^2))
    sig_map, obj_to_sig = group_objects_by_signature(all_mesh_objs)

    processed_signatures = set()
    total_changed = 0

    for src in selected:
        sig = obj_to_sig.get(src)
        if sig is None:
            continue

        # If a signature has already been standardized by an earlier selected source, skip it
        if sig in processed_signatures:
            continue
        processed_signatures.add(sig)

        src_data = src.data
        group = sig_map.get(sig, [])

        # Assign the source's datablock to all matching targets in the group
        for dst in group:
            # Keep the source itself unchanged
            if dst is src:
                continue
            # Skip if already sharing this datablock
            if dst.data is src_data:
                continue
            # Replace mesh datablock => turn into an instance of src_data
            dst.data = src_data
            total_changed += 1

        # Optional: if multiple selected objects belong to the same signature,
        # make them share the same datablock as well (unify the group fully).
        # Comment out this block if you want each selected object to retain its own data.
        for other_src in selected:
            if other_src is src:
                continue
            if obj_to_sig.get(other_src) == sig and other_src.data is not src_data:
                other_src.data = src_data

    print(f"Instancing complete. Datablocks assigned to {total_changed} object(s).")


# Run
make_instances_from_selection()
    