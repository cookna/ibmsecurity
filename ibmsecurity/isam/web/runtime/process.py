import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve runtime component status
    """
    return isamAppliance.invoke_get("Retrieving web runtime component status",
                                    "/isam/runtime_components/")


def _check(isamAppliance):
    """
    Check if the runtime process is configured or not
    :param isamAppliance:
    :return:
    """
    ret_obj = get(isamAppliance)

    if ret_obj['data']['modecode'] == '-1':
        return False
    else:
        return True


def config(isamAppliance, admin_pwd, ps_mode="local", user_registry="local", ldap_host=None, ldap_port=None,
           ldap_dn=None, ldap_pwd=None, ldap_ssl_db=None, ldap_ssl_label=None, ldap_suffix=None, clean_ldap=False,
           domain="Default", admin_cert_lifetime="1460", ssl_compliance="none", isam_host=None, isam_port="7135",
           check_mode=False, force=False):
    """
    Configure Runtime Component
    :param isamAppliance:
    :return:
    """
    if (force is True or _check(isamAppliance) is False):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Configure web runtime Component", "/isam/runtime_components/",
                                             {
                                                 "ps_mode": ps_mode,
                                                 "user_registry": user_registry,
                                                 "ldap_host": ldap_host,
                                                 "ldap_port": ldap_port,
                                                 "ldap_dn": ldap_dn,
                                                 "ldap_pwd": ldap_pwd,
                                                 "ldap_ssl_db": ldap_ssl_db,
                                                 "ldap_ssl_label": ldap_ssl_label,
                                                 "ldap_suffix": ldap_suffix,
                                                 "clean_ldap": clean_ldap,
                                                 "domain": domain,
                                                 "admin_pwd": admin_pwd,
                                                 "admin_cert_lifetime": admin_cert_lifetime,
                                                 "ssl_compliance": ssl_compliance,
                                                 "isam_host": isam_host,
                                                 "isam_port": isam_port
                                             })

    return isamAppliance.create_return_object()


def unconfig(isamAppliance, clean=False, ldap_dn=None, ldap_pwd=None, check_mode=False, force=False):
    """
    Unconfigure existing runtime component
    """
    if (force is True or _check(isamAppliance) is True):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Unconfigure web runtime component",
                                            "/isam/runtime_components/RTE",
                                            {
                                                "operation": "unconfigure",
                                                "force": force,
                                                "clean": clean,
                                                "ldap_dn": ldap_dn,
                                                "ldap_pwd": ldap_pwd
                                            })

    return isamAppliance.create_return_object()


def import_config(isamAppliance, migrate_file, check_mode=False, force=False):
    """
    Import or migrate runtime component
    """
    if (force is True or _check(isamAppliance) is True):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files("Import or Migrate web runtime component",
                                                   "/isam/runtime_components/",
                                                   [{
                                                       'file_formfield': 'migrate_file',
                                                       'filename': migrate_file,
                                                       'mimetype': 'application/octet-stream'
                                                   }],
                                                   {})

    return isamAppliance.create_return_object()


def execute(isamAppliance, operation='restart', check_mode=False, force=False):
    """
    Execute an operation on runtime component

    :param isamAppliance:
    :param operation:
    :return:
    """
    if (force is False):
        ret_obj = get(isamAppliance)
        if (ret_obj['data']['statuscode'] == '1'):
            logger.info("ISAM web runtime is unconfigured.")
            return isamAppliance.create_return_object()
        if (ret_obj['data']['statuscode'] == '0' and operation == 'start'):
            logger.info("ISAM web runtime is already started.")
            return isamAppliance.create_return_object()
        if (ret_obj['data']['statuscode'] == '2' and operation == 'stop'):
            logger.info("ISAM web runtime is already stopped.")
            return isamAppliance.create_return_object()

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put("Execute an operation on web runtime component",
                                        "/isam/runtime_components/",
                                        {
                                            "operation": operation
                                        })


def compare(isamAppliance1, isamAppliance2):
    """
    Compare web runtime between 2 appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    # Ignore status. since process start/stop status can be different
    del ret_obj1['data']['status']
    del ret_obj1['data']['statuscode']
    del ret_obj2['data']['status']
    del ret_obj2['data']['statuscode']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['status', 'statuscode'])
