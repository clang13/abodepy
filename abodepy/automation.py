"""Representation of an automation configured in Abode."""
import json

from abodepy.exceptions import AbodeException

import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR


class AbodeAutomation:
    """Class for viewing and controlling automations."""

    def __init__(self, abode, automation):
        self._abode = abode
        self._automation = automation

    def set_active(self, active):
        """Activate and deactivate an automation."""
        url = CONST.AUTOMATION_EDIT_URL
        url = url.replace(
            '$AUTOMATIONID$', self.automation_id)

        self._automation['is_active'] = str(int(active))

        response = self._abode.send_request(
            method="put", url=url, data=self._automation)

        response_object = json.loads(response.text)

        if (response_object['id'] != self.automation_id or
                response_object['is_active'] != self._automation['is_active']):
            raise AbodeException((ERROR.INVALID_AUTOMATION_EDIT_RESPONSE))

        self._automation = response_object

    def trigger(self, only_manual=True):
        """Trigger a quick-action automation."""
        if not self.is_quick_action and only_manual:
            return False

        url = CONST.AUTOMATION_APPLY_URL
        url = url.replace(
            '$AUTOMATIONID$', self.automation_id)

        self._abode.send_request(
            method="put", url=url, data=self._automation)

        return True

    def refresh(self):
        """Refresh the automation."""
        url = CONST.AUTOMATION_ID_URL
        url = url.replace(
            '$AUTOMATIONID$', self.automation_id)

        response = self._abode.send_request(method="get", url=url)
        response_object = json.loads(response.text)

        if response_object['id'] != self.automation_id:
            raise AbodeException((ERROR.INVALID_AUTOMATION_REFRESH_RESPONSE))

        self._automation = response_object

    @property
    def automation_id(self):
        """Get the id of the automation."""
        return self._automation['id']

    @property
    def name(self):
        """Get the name of the automation."""
        return self._automation['name']

    @property
    def type(self):
        """Get the type of the automation."""
        return self._automation['type']

    @property
    def sub_type(self):
        """Get the sub type of the automation."""
        return self._automation['sub_type']

    @property
    def is_active(self):
        """Return if the automation is active."""
        return int(self._automation.get('is_active', '0')) == 1

    @property
    def is_quick_action(self):
        """Return if the automation is a quick action."""
        return self.type == CONST.AUTOMATION_TYPE_MANUAL
