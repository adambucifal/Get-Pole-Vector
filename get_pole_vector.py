"""
=====================================================================
-----> Places a locator at the correct pole vector of 3 joints <-----
=====================================================================
"""

import maya.cmds as cmds
from maya.OpenMaya import MVector, MGlobal


def get_pole_vec_pos(
    root_pos: list[float], 
    mid_pos: list[float], 
    end_pos: list[float], 
    multiplier: float = 1.0,
) -> maya.OpenMaya.MVector:
    """
    Calculates the correct pole vector position based on the input joints
    
    :param root_pos: list[float] - xyz world position of the root joint
    :param mid_pos: list[float] - xyz world position of the mid joint
    :param end_pos: list[float] - xyz world position of the end joint
    :param multiplier: float - scalar value that multiplies the pole vector to 
        control how close it is to the joints
        
    :return: maya.OpenMaya.MVector
    """
    # Create MVector objects
    root_vec = MVector(*root_pos)
    mid_vec = MVector(*mid_pos)
    end_vec = MVector(*end_pos)
    
    # Direction from the root to end
    line = end_vec - root_vec
    
    # Vector to compare the closest point on the line
    source_point = mid_vec - root_vec
    
    # Scalar to get closest point between the root and end joints relative to the mid joint
    closest_point_scale_val = (line * source_point) / (line * line)
    
    # Calulcate the mid point with the new scalar value
    closest_mid_point = (line * closest_point_scale_val) + root_vec
    
    # Lengths (Magnitude) between vectors
    root_to_mid_mag = (mid_vec - root_vec).length()
    mid_to_end_mag = (end_vec - mid_vec).length()
    total_mag = (root_to_mid_mag + mid_to_end_mag) * multiplier
    
    # Calculate the pole vector
    pole_vector = (mid_vec - closest_mid_point).normal() * total_mag + mid_vec
    
    MGlobal.displayInfo(f"{pole_vector.x}, {pole_vector.y}, {pole_vector.z}")
    
    return pole_vector


def place_locator(position: maya.OpenMaya.MVector) -> str:
    """
    Places a locator at the input position
    
    :param position: maya.OpenMaya.MVector
    
    :return: str - name of the locator
    """
    locator = cmds.spaceLocator()[0]
    cmds.xform(
        locator, 
        translation=[position.x, position.y, position.z], 
        worldSpace=True,
    )
    cmds.select(locator)
    
    return locator


def main() -> None:
    """
    Calculates the pole vector and places a locator at that position
    
    :return None:
    """
    joints = cmds.ls(selection=True, type="joint")
    
    if len(joints) != 3:
        cmds.error("Select three joints")
    
    positions = [
        cmds.xform(jnt, query=True, rotatePivot=True, worldSpace=True) 
        for jnt in joints
    ] 
   
    place_locator(get_pole_vec_pos(*positions, 1))


if __name__ == "__main__":
    main()