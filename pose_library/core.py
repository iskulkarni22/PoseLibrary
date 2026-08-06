import os
import json

ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/poses'
EXT = 'json'


def get_poses_dict():
    """ Get dictionary with available poses.

        Example:
            {'pose_name': 'file_path'}
        
        Returns:
            dict

    """
    poses_dict = {}

    for file_name in os.listdir(ROOT_DIR):
        if not file_name.endswith(EXT):
            continue
        pose_name = file_name.split('.')[0]
        file_path = os.path.join(ROOT_DIR, file_name)

        poses_dict[pose_name] = file_path

    return poses_dict


def write_pose_to_file(pose_name, pose_dict):
    """ Write pose data to a file.

        Args:
            pose_name(str): name of the resulting file
            pose_dict(dict): contents of the pose

    """
    file_name = '{}.{}'.format(pose_name, EXT)
    file_path = os.path.join(ROOT_DIR, file_name)

    with open(file_path, 'w') as f:
        json.dump(pose_dict, f, indent=4)


def read_pose_from_file(file_path):
    """ Read pose data from file.
    
        Args:
            file_path(str): path to file to read
        

        Returns:
            dict: pose dictionary

    """
    with open(file_path, 'r') as f:
        pose_dict = json.load(f)
    return pose_dict

def remove_pose_from_library(file_path):
    """ Remove pose file from pose library.

        Args:
            pose_name(str): name of file to remove
        
        Returns:
            bool: whether removal was successful or not

    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
