import copy
import opsc
import oobb
import oobb_base

thickness_tin = 1.5
thickness_indent_bottom = 1
#thickness_bead = 3

clearance_internal = 1

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True:
        filter = ""
        #filter = "test"

        #kwargs["save_type"] = "none"
        kwargs["save_type"] = "all"
        
        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 1

    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        part_default = {} 
        part_default["project_name"] = "test" ####### neeeds setting
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        #9x12 a5
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        #p3["thickness"] = 6
        p3["width"] = 9
        p3["height"] = 12
        part["kwargs"] = p3
        width_start =  160
        p3["width_start"] = width_start
        height_start = 220
        p3["height_start"] = height_start
        depth_start = 22.5
        p3["depth_start"] = depth_start
        p3["thickness_bead"] = 3
        extra = f"width_start_{width_start}_height_start_{height_start}_depth_start_{depth_start}"
        p3["extra"] = extra
        part["name"] = "main_spacer"
        parts.append(part)
        
        #10x14 a5
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        #p3["thickness"] = 6
        p3["width"] = 10
        p3["height"] = 14
        part["kwargs"] = p3
        width_start =  160
        p3["width_start"] = width_start
        height_start = 220
        p3["height_start"] = height_start
        depth_start = 22.5
        p3["depth_start"] = depth_start        
        p3["thickness_bead"] = 3
        extra = f"width_start_{width_start}_height_start_{height_start}_depth_start_{depth_start}"
        p3["extra"] = extra
        part["name"] = "main_spacer"
        parts.append(part)

        #10x14 smaller
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        #p3["thickness"] = 6
        p3["width"] = 8
        p3["height"] = 10
        part["kwargs"] = p3
        width_start =  128 + 2.5
        p3["width_start"] = width_start
        height_start = 168 - 5
        p3["height_start"] = height_start
        depth_start = 18.5 + 0.5       
        p3["depth_start"] = depth_start        
        p3["thickness_bead"] = 2 
        extra = f"width_start_{width_start}_height_start_{height_start}_depth_start_{depth_start}"
        p3["extra"] = extra
        part["name"] = "main_spacer"
        parts.append(part)
        
    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")
            if filter in name:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")

def get_main_spacer(thing, **kwargs):

    depth = kwargs.get("thickness", 4)
    prepare_print = kwargs.get("prepare_print", True)

    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20
    width = kwargs.get("width", None)
    height = kwargs.get("height", None)
    width_start =  kwargs.get("width_start", None)
    height_start = kwargs.get("height_start", None)
    depth_start = kwargs.get("depth_start", None)

    thickness_bead = kwargs.get("thickness_bead", None)

    width_total = width_start - thickness_tin
    height_total = height_start - thickness_tin
    depth_total = (depth_start 
                   - thickness_bead 
                   - thickness_indent_bottom)

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"rounded_rectangle"    
    w = width_total
    h = height_total
    d = depth_total
    size = [w, h, d]
    p3["size"] = size
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    rad = 11 - thickness_tin / 2
    p3["radius"] = rad
    oobb_base.append_full(thing,**p3)
    
    #add cutout
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"rounded_rectangle"    
    w = width * 15 + clearance_internal
    h = height * 15 + clearance_internal
    d = depth_total
    size = [w, h, d]
    p3["size"] = size
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    rad = 5 + clearance_internal / 2
    p3["radius"] = rad
    oobb_base.append_full(thing,**p3)
    

    if prepare_print:
        shift = height_total/2

        #add slice # right
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cube"
        w = width_total
        h = height_total
        d = depth_total
        size = [w, h, d]
        pos1 = copy.deepcopy(pos)
        pos1[0] += shift
        p3["pos"] = pos1
        p3["size"] = size
        p3["m"] = "#"
        #oobb_base.append_full(thing,**p3)
        
        #add slice # bottom
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cube"
        w = width_total
        h = height_total
        d = depth_total
        size = [w, h, d]
        pos1 = copy.deepcopy(pos)
        pos1[1] += -shift
        p3["pos"] = pos1
        p3["size"] = size
        p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

        
    
###### utilities



def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]
    func(thing, **kwargs)

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        opsc.opsc_make_object(f'scad_output/{thing["id"]}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)    


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)