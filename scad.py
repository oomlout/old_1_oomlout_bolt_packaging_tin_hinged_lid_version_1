import copy
import opsc
import oobb
import oobb_base
import os

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

        kwargs["save_type"] = "none"
        #kwargs["save_type"] = "all"
        

        #navigation = False
        navigation = True    

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
        
        
        #10x14 a5
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        #p3["thickness"] = 6
        p3["width"] = 10
        p3["height"] = 14
        part["kwargs"] = p3  
        p3["width_start"] = 161 # external_measurement
        p3["height_start"] = 221
        p3["depth_start"] = 21  #internal depth measurement      
        p3["thickness_tin"] = 0.5
        p3["thickness_bead"] = 2
        p3["diameter_bottom_bend"] = 1
        extra = f"width_start_{p3["width_start"]}_height_start_{p3["height_start"]}_depth_start_{p3["depth_start"]}"
        p3["extra"] = extra
        part["name"] = "main_spacer"
        parts.append(part)


        #8x10 smaller
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        #p3["thickness"] = 6
        p3["width"] = 8
        p3["height"] = 10
        part["kwargs"] = p3  
        p3["width_start"] = 129 # external_measurement
        p3["height_start"] = 169
        p3["depth_start"] = 18 #inside depth measurement        
        p3["thickness_tin"] = 0.5
        p3["thickness_bead"] = 1.5 #remember to remove tin thickness
        p3["diameter_bottom_bend"] = 1
        extra = f"width_start_{p3["width_start"]}_height_start_{p3["height_start"]}_depth_start_{p3["depth_start"]}"
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

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        generate_navigation(sort = sort)


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
    thickness_tin = kwargs.get("thickness_tin", None)
    diameter_bottom_bend = kwargs.get("diameter_bottom_bend", None)

    clearance_width_extra = kwargs.get("clearance_width_extra", 0)    
    clearance_height_extra = kwargs.get("clearance_height_extra", 0)
    clearance_sides_extra = kwargs.get("clearance_sides_extra", 0.5) #the distance to bring in the cube sides to allow for glue or the bead lip to press up doubled so it's on each side
    clearance_depth_extra = kwargs.get("clearance_depth_extra", 0.5)

    width_total = width_start - thickness_tin - clearance_width_extra
    height_total = height_start - thickness_tin - clearance_height_extra
    depth_total = (depth_start 
                   - thickness_bead 
                   - clearance_depth_extra)
    depth_total_bead_buldge_clearance = depth_total - thickness_bead / 2
    depth_total_to_bead_top = depth_total + thickness_bead

    #add plate #inset to avoide bottom bend and add some corner clearance
    extra_clearance_corner = 1.5
    radius_inside = 9
    w = width_total - diameter_bottom_bend
    h = height_total - diameter_bottom_bend
    d = depth_total_bead_buldge_clearance 
    size_main = [w, h, d]
    size_big = copy.deepcopy(size_main)
    size_big[0] += - extra_clearance_corner*2
    size_big[1] += - extra_clearance_corner*2
    size_little = copy.deepcopy(size_main)
    size_little[0] += - thickness_bead*2
    size_little[1] += - thickness_bead*2
    size_little[2] = depth_total_to_bead_top

    
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"rounded_rectangle"       
    
    p3["size"] = size_big
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    diff = (size_big[0]-size_little[0])/2
    rad = radius_inside + diff
    p3["radius"] = rad
    oobb_base.append_full(thing,**p3)

    #above the bead piece
    p4 = copy.deepcopy(p3)
    size = copy.deepcopy(size_main)    
    p4["size"] = size_little
    p4["pos"][2] += 0
    rad = radius_inside
    p4["radius"] = rad
    #p4["m"] = "#"
    oobb_base.append_full(thing,**p4)


    #add cubes to snuck the height beyond the corner
    corner_radius_clearance = 30
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_cube"
    w = width_total - corner_radius_clearance * 2
    h = height_total - clearance_sides_extra * 2
    d = depth_total - diameter_bottom_bend
    size = [w, h, d]
    p3["size"] = size
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += diameter_bottom_bend
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    p4 = copy.deepcopy(p3)
    w = width_total - clearance_sides_extra * 2
    h = height_total  - corner_radius_clearance * 2
    size = [w, h, d]
    p4["size"] = size
    #p4["m"] = "#"
    oobb_base.append_full(thing,**p4)
    



    

    #add cutout
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"rounded_rectangle"    
    w = width * 15 + clearance_internal
    h = height * 15 + clearance_internal
    d = depth_total + thickness_bead
    size = [w, h, d]
    p3["size"] = size
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    rad = 5 + clearance_internal / 2
    p3["radius"] = rad
    oobb_base.append_full(thing,**p3)
    

    if prepare_print:
        shift = width_total/2

        #add slice # right
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cube"
        w = width_total
        h = height_total
        d = depth_total + thickness_bead
        size = [w, h, d]
        pos1 = copy.deepcopy(pos)
        pos1[0] += shift
        p3["pos"] = pos1
        p3["size"] = size
        #p3["m"] = "#"
        #oobb_base.append_full(thing,**p3)
        
        shift = height_total/2
        #add slice # bottom
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cube"
        w = width_total
        h = height_total
        d = depth_total + thickness_bead
        size = [w, h, d]
        pos1 = copy.deepcopy(pos)
        pos1[1] += -shift
        p3["pos"] = pos1
        p3["size"] = size
        #p3["m"] = "#"
        #oobb_base.append_full(thing,**p3)

        
    
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

def generate_navigation(folder="scad_output", sort=["width", "height", "thickness"]):
    #crawl though all directories in scad_output and load all the working.yaml files
    parts = {}
    for root, dirs, files in os.walk(folder):
        if 'working.yaml' in files:
            yaml_file = os.path.join(root, 'working.yaml')
            with open(yaml_file, 'r') as file:
                part = yaml.safe_load(file)
                # Process the loaded YAML content as needed
                part["folder"] = root
                part_name = root.replace(f"{folder}","")
                
                #remove all slashes
                part_name = part_name.replace("/","").replace("\\","")
                parts[part_name] = part

                print(f"Loaded {yaml_file}: {part}")

    pass
    for part_id in parts:
        part = parts[part_id]
        kwarg_copy = copy.deepcopy(part["kwargs"])
        folder_navigation = "navigation"
        folder_source = part["folder"]
        folder_extra = ""
        for s in sort:
            ex = kwarg_copy.get(s, "default")
            folder_extra += f"{s}_{ex}/"

        #replace "." with d
        folder_extra = folder_extra.replace(".","d")            
        folder_destination = f"{folder_navigation}/{folder_extra}"
        if not os.path.exists(folder_destination):
            os.makedirs(folder_destination)
        if os.name == 'nt':
            #copy a full directory
            command = f'xcopy "{folder_source}" "{folder_destination}" /E /I'
            print(command)
            os.system(command)
        else:
            os.system(f"cp {folder_source} {folder_destination}")



if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)