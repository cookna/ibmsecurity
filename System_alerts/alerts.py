import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Get all  objects
    """
    return isdsAppliance.invoke_get("Get all alert objects",
                                    "/system_alerts/")


def get_all(isdsAppliance):
    """
    Returns all objects
    """
    return isdsAppliance.invoke_get("Get all Objects", "/net_objs/alerts/")


def enable(isdsAppliance, name, objType, check_mode=False, force=False):
    """
    Enable a system alert
    """
    uuid = search(isdsAppliance, name)

    if force is True or _check(isdsAppliance, uuid) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post(
                "Enable a system alert",
                "/system_alerts",
                {
                    'uuid': uuid,
                    'objType': objType
                })

    return isdsAppliance.create_return_object()


def disable(isdsAppliance, name, check_mode=False, force=False):
    """
    Delete a system alert
    """
    uuid = search(isdsAppliance, name)
    if force is True or _check(isdsAppliance, uuid) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_delete(
                "Delete a system alert",
                "/system_alerts/{0}".format(uuid))

    return isdsAppliance.create_return_object()


def _check(isdsAppliance, uuid):
    """
    Check if the system alert exists
    """
    ret_obj = get(isdsAppliance)
    for obj in ret_obj['data']['responses']:
        if obj['uuid'] == uuid:
            return True

    return False


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare system alert objects between two appliance
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

    for obj in ret_obj1['data']['responses']:
        del obj['uuid']
    for obj in ret_obj2['data']['responses']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])


def search(isdsAppliance, name):
    """
    search for alert name and return uuid
    """
    check_obj = get_all(isdsAppliance)

    for obj in check_obj['data']['alerts']:
        if obj['name'] == name:
            logger.info("Name is {}".format(obj['objType']))
            return obj['uuid']
