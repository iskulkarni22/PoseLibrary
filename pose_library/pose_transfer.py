from maya import cmds

def transfer_selected(*args):
    """ Transfer pose from first selected rig to the rest of the selection.

        Args:
            *args: Catch-all for arguments passed in by Maya.

    """
    # selected namespaces
    namespaces = get_selected_namespaces()
    # validate selection
    if len(namespaces) < 2:
        cmds.warning('Please select 2 or more rigs!')
        return
    source_namespace = namespaces[0]
    target_namespaces = namespaces[1:]
    # get pose dictionary from source
    pose_dict = get_pose_dict(source_namespace)
    # apply to targets
    for target in target_namespaces:
        apply_pose(pose_dict, target)


def get_selected_namespaces():
    """ Get list of namespaces for selected rigs.

        Returns:
            list

    """
    selection = cmds.ls(selection=True)
    if len(selection) == 0:
        return []

    namespace_list = []
    for ctrl in selection:
        namespace = ctrl.split(":")[0]
        if namespace not in namespace_list:
            namespace_list.append(namespace)

    return namespace_list 

def get_attrs_from_node(ctrl_node):
    """ Get attribute names from node.

        Args:
            ctrl_node(str): Name of the node.

        Returns:
            list: List of short attribute names.

    """
    attributes = cmds.listAnimatable(ctrl_node)
    if not attributes:
        return []
    
    attr_names = []
    for attr in attributes:
        attr_name = attr.split(".")[-1]
        attr_names.append(attr_name)

    return attr_names

def get_pose_dict(namespace):
    """ Get the pose dictionary without namespaces.

        Args:
            namespace(str): Filter selection by this namespace.

        Returns:
            dict: Dictionary of controls with attributes and their values.

    """
    # get selection 
    selection = cmds.ls(selection=True)
    if not selection:
        return {}

    pose_dict = {}
    for ctrl in selection:
        # filter selection based on namespace
        if not ctrl.startswith(namespace):
            continue
        # get attributes
        animatable_attrs = get_attrs_from_node(ctrl)
        if not animatable_attrs:
            continue

        # populate dictionary
        for attr in animatable_attrs:
            ctrl_name = ctrl.split(":")[-1]
            full_attr = '{}.{}'.format(ctrl_name, attr)
            ctrl_with_attr = '{}.{}'.format(ctrl, attr)
            pose_dict[full_attr] = cmds.getAttr(ctrl_with_attr)

    return pose_dict

def apply_pose(pose_dict, namespace):
    """ Apply provided pose to provided namespace.

        Args:
            pose_dict(dict): dictionary with pose data.
            namespace(str): target namespace to apply the pose to.

    """
    # get attribute names
    for attr_name in pose_dict:
        # need to add namespace
        attr_value = pose_dict[attr_name]
        full_attr_name = '{}:{}'.format(namespace, attr_name)
        
        node, short_attr_name = full_attr_name.split(".")
        # attribute checks
        if not cmds.objExists(node) or \
            not cmds.attributeQuery(short_attr_name, node=node, exists=True) or \
            not cmds.getAttr(full_attr_name, settable=True):
            continue

        # set attribute
        cmds.setAttr(full_attr_name, attr_value)
