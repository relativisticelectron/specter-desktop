from pywebpush import webpush, WebPushException
import json
from flask import current_app

# see https://suryasankar.medium.com/how-to-setup-basic-web-push-notification-functionality-using-a-flask-backend-1251a5413bbe
def trigger_push_notification(push_subscription, title, body):
    print(f'trigger_push_notification   {title}, {body},   push_subscription {push_subscription}')
    try:
        response = webpush(
            subscription_info=push_subscription,
            data=json.dumps({"title": title, "body": str(body)}),
            vapid_private_key="DyYMSrnuEq084pbHTNvxdjrxcatlCAXQkL1osvtbEzE",   # https://web-push-codelab.glitch.me/
            vapid_claims={
                "sub": "mailto:{}".format(
                    'my-email@some-url.com')
            }
        )
        print(f'webpush {response}')
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


def trigger_push_notifications_for_subscriptions(subscriptions, title, body):
    return [trigger_push_notification(subscription, title, body)
            for subscription in subscriptions]


def trigger_push_notifications_for_user(user, title, body):
    return [
        trigger_push_notification(subscription, title, body)
        for subscription in user.push_subscriptions]


def trigger_push_notifications_for_users(users, title, body, contents=None):
    return { user.id: trigger_push_notifications_for_user(user, title, body) for user in users}
