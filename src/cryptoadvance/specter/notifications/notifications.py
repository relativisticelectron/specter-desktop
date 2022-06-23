import logging

logger = logging.getLogger(__name__)
import datetime
import hashlib


class NotificationTypes:
    debug = "debug"
    information = "information"
    warning = "warning"
    error = "error"
    exception = "exception"


class Notification:
    """
    A Notification is a datastructure to store title, body, ...
    The field names should be ideally identical to https://notifications.spec.whatwg.org/#api
    Additional fields, like id, can be added
    """

    def __init__(
        self,
        title,
        default_target_ui,
        all_target_uis,
        user_id,
        target_uis="default",
        notification_type=None,
        body=None,
        data=None,
        image=None,
        icon=None,
        timeout=None,
    ):
        self.title = str(title)
        self.user_id = user_id
        self.date = datetime.datetime.now()
        self.last_shown_date = dict()  # structure {'target_ui' : date}
        self.was_closed_in_target_uis = set()  # example: {'WebAPI', 'logging'}

        if not target_uis:
            target_uis = "default"
        self.target_uis = (
            {target_uis} if isinstance(target_uis, str) else set(target_uis)
        )
        self.cleanup_target_uis(default_target_ui, all_target_uis)

        # clean up invalid NotificationTypes
        self.notification_type = (
            notification_type if notification_type else NotificationTypes.information
        )
        if self.notification_type not in {
            NotificationTypes.debug,
            NotificationTypes.information,
            NotificationTypes.warning,
            NotificationTypes.error,
            NotificationTypes.exception,
        }:
            self.notification_type = NotificationTypes.information

        self.body = body
        self.data = data
        self.image = image
        self.icon = icon
        self.timeout = timeout  # [ms]

        # set id (dependent on all other properties, so must eb set last)
        self.id = None
        self._set_id()

    def __str__(self):
        return str(self.__dict__)

    def _set_id(self):
        reduced_dict = self.__dict__.copy()
        del reduced_dict["id"]
        self.id = hashlib.sha256(str(reduced_dict).encode()).hexdigest()

    def set_shown(self, target_ui, date=None):
        self.last_shown_date[target_ui] = date if date else datetime.datetime.now()
        logger.debug(f"set_notification_shown {self}")

    def set_closed(self, target_ui):
        self.was_closed_in_target_uis.add(target_ui)
        logger.debug(f"set_closed {self}")

    def cleanup_target_uis(self, default_target_ui, all_target_uis):
        # clean up the notification['target_uis']
        if "internal_notification" in self.target_uis:
            # no cleanup for internal_notification
            return

        if "all" in self.target_uis:
            target_uis = all_target_uis

        # replace the "default" target_ui with the 0.th  ui_notifications
        if "default" in self.target_uis:
            self.target_uis.remove("default")
            if default_target_ui:
                self.target_uis.add(default_target_ui)

    def to_js_notification(self):
        """
        Returns a datastructure such that a Notification(result) can be called https://notifications.spec.whatwg.org/#api

        The returned structure is:
            {
                "title": title,
                "id": id,
                "notification_type": notification_type,
                "timeout": timeout,
                "options": {
                    body = "",
                    image = None,
                },
            }
        "options" fields are optional, and can be looked up here: https://notifications.spec.whatwg.org/#dictdef-notificationoptions
        """
        js_notification = {
            "title": self.title,
            "id": self.id,
            "notification_type": self.notification_type,
            "timeout": self.timeout,
            "options": {},
        }

        for key, value in self.__dict__.items():
            if key in js_notification or value is None:
                continue
            js_notification["options"][key] = value

        return js_notification
