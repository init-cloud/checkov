from __future__ import annotations

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class LBListenerUsingHTTPS(BaseResourceCheck):

    def __init__(self):
        name = "Ensure LB Listener Using HTTPS"
        id = "CKV_NCP_30"
        supported_resources = ("ncloud_lb_listener",)
        categories = (CheckCategories.GENERAL_SECURITY,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if "protocol" in conf.keys():
            if conf.get("protocol") != ['HTTP']:
                return CheckResult.PASSED
        return CheckResult.FAILED


check = LBListenerUsingHTTPS()
