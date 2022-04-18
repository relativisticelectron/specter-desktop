from pywebpush import webpush, WebPushException
import json
from flask import current_app

# see https://suryasankar.medium.com/how-to-setup-basic-web-push-notification-functionality-using-a-flask-backend-1251a5413bbe
def trigger_push_notification(push_subscription, notification):
    try:
        #print(notification)
        response = webpush(
            subscription_info=push_subscription,
            data=json.dumps(notification),
            vapid_private_key="DyYMSrnuEq084pbHTNvxdjrxcatlCAXQkL1osvtbEzE",   # https://web-push-codelab.glitch.me/
            vapid_claims={
                "sub": "mailto:{}".format(
                    'my-email@some-url.com')
            }
        )
        return response.ok
    except WebPushException as ex:
        if ex.response and ex.response.json():
            extra = ex.response.json()
            print("Remote service replied with a {}:{}, {}",
                  extra.code,
                  extra.errno,
                  extra.message
                  )
        return False


def trigger_push_notifications_for_subscriptions(subscriptions, notification):
    return [trigger_push_notification(subscription, notification)
            for subscription in subscriptions]


def trigger_push_notifications_for_user(user, notification):
    return [
        trigger_push_notification(subscription, notification)
        for subscription in user.push_subscriptions]


def trigger_push_notifications_for_users(users, notification):
    return { user.id: trigger_push_notifications_for_user(user, notification) for user in users}
