import bpy

# =================================================================
# loading data

def load_data(filepath:str) -> dict:
    """Loads data from a .json file.
    
    Data must contain "NODES" and "ELEMENTS"

    Args:
        filepath (str): Path to file to be loaded.

    Returns:
        dict: contends of the file as a python dictionary
    """
    
    # import required modules
    import json
    import numpy as np
    import os
    
    # # check if file is json
    # assert filepath.endswith('.json'), ValueError(
    #     "Expected .json file. received: {}".format(filepath))
    # check if file exists
    
    assert os.path.exists(filepath), ValueError(
        "Filepath provided does not exist: {}".format(filepath))
    # check if path is file (not a directory)
    assert os.path.isfile(filepath), ValueError(
        "Filepath is not a file: {}".format(filepath))
    
    # open and read json file
    with open(filepath, "r") as jfile:
        data = json.load(jfile)
    
    # we expect NODES and ELEMENTS to be in data
    assert "NODES" in data, ValueError(
        "NODES not found in data. Please, check file")
    assert "ELEMENTS" in data, ValueError(
        "ELEMENTS not found in data. Please, check file")

    # convert nodes and elements to numpy arrays
    data["NODES"] = np.array(data["NODES"])
    data["ELEMENTS"] = np.array(data["ELEMENTS"])
    
    return data

# =================================================================
# creating mesh/object

# -- break elements into edges

def break_hex8_into_edges(hex8_feb) -> list:
    """
        Breaks down a hex8 element into list of edges.

        reference: https://help.febio.org/FEBio/FEBio_um_2_9/FEBio_um_2-9-3.8.2.1.html
    """
    
    edges = [
        # bottom
        [hex8_feb[0], hex8_feb[1]],
        [hex8_feb[1], hex8_feb[2]],
        [hex8_feb[2], hex8_feb[3]],
        [hex8_feb[3], hex8_feb[0]],
        # top
        [hex8_feb[4], hex8_feb[5]],
        [hex8_feb[5], hex8_feb[6]],
        [hex8_feb[6], hex8_feb[7]],
        [hex8_feb[7], hex8_feb[4]],
        # vertical edges
        [hex8_feb[0], hex8_feb[4]],
        [hex8_feb[1], hex8_feb[5]],
        [hex8_feb[2], hex8_feb[6]],
        [hex8_feb[3], hex8_feb[7]],
    ]
        
    return edges

def create_edges_from_elements(elements) -> list:
    edges = []
    for cell in elements:
        if len(cell) == 8:
            edges.extend(break_hex8_into_edges(cell))
        else:
            print("non-hex8 found. will need to add method for cell of length: {}".format(len(cell)))
    return edges

# -- break elements into faces

def break_hex8_into_faces(hex8_feb) -> list:
    """
        Breaks down a hex8 element into list of faces.

        reference: https://help.febio.org/FEBio/FEBio_um_2_9/FEBio_um_2-9-3.8.2.1.html
    """
        
    faces = [
        # bottom
        [
            hex8_feb[0], 
            hex8_feb[1],
            hex8_feb[2],
            hex8_feb[3],
        ],
        # top
        [
            hex8_feb[4], 
            hex8_feb[5],
            hex8_feb[6],
            hex8_feb[7],
        ],
        # side 1
        [
            hex8_feb[0], 
            hex8_feb[1],
            hex8_feb[5],
            hex8_feb[4],
        ],
        # side 2
        [
            hex8_feb[1], 
            hex8_feb[2],
            hex8_feb[6],
            hex8_feb[5],
        ],
        # side 3
        [
            hex8_feb[2], 
            hex8_feb[3],
            hex8_feb[7],
            hex8_feb[6],
        ],
        # side 4
        [
            hex8_feb[3], 
            hex8_feb[0],
            hex8_feb[4],
            hex8_feb[7],
        ],
    ]
        
    return faces

def create_faces_from_elements(elements) -> list:
    faces = []
    for cell in elements:
        if len(cell) == 8:
            faces.extend(break_hex8_into_faces(cell))
        else:
            print("non-hex8 found. will need to add method for cell of length: {}".format(len(cell)))
    return faces

# -- create new object
    
def create_new_object_from_data(name, data):
    # import modules
    import numpy as np
    
    # create new object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    # link object to scene
    bpy.context.scene.collection.objects.link(obj)
    # set object as currently active
    bpy.context.view_layer.objects.active = obj
    
    # add mesh data
    
    # set mesh edges based on elements
    elems = data["ELEMENTS"][0]
    # check if elements has an additional dimension (supposed to be 8, but it can include elements id)
    if elems.shape[-1] == 9:
        elems = elems[:, 1:]
    # check for right elems dims -> will need to implement option for tet4
    if elems.shape[-1] != 8:
        raise RuntimeError("We currently only support hex8 elements. "
                           "Found elements with size: {}".format(elems.shape[-1]))
    # col 1 is element id ->> will remove it later
    edges = create_edges_from_elements(elems)
    
    # set mesh faces based on user data or elements
    faces = []
    # check if user provided surface data
    if "SURFACE" in data:
        print("WARNING: surface data from user data is not yet implemented --")
    else:
        # try to add faces from elements
        faces = create_faces_from_elements(elems)

    if len(edges) == 0 and len(faces) == 0:
        raise RuntimeError("No edges and faces were found. Please, check input file.")
    
    # create nem mesh
    mesh.from_pydata(data["NODES"], edges, faces)
    
    return mesh