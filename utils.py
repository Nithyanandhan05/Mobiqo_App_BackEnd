# utils.py
from firebase_admin import messaging

def send_universal_push_notification(user, title, body, data_payload=None):
    """
    Sends a Firebase push notification to ALL of a user's registered devices (Android & Web).
    """
    if data_payload is None:
        data_payload = {}

    tokens_to_notify = []
    # Check for both platform tokens in the User model
    if getattr(user, 'fcm_token_android', None):
        tokens_to_notify.append(user.fcm_token_android)
    if getattr(user, 'fcm_token_web', None):
        tokens_to_notify.append(user.fcm_token_web)

    if not tokens_to_notify:
        return False

    success_count = 0
    for token in tokens_to_notify:
        try:
            # Use messaging.Message for broad compatibility across Firebase versions
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data=data_payload,
                token=token
            )
            messaging.send(message)
            success_count += 1
        except Exception as e:
            print(f"⚠️ FCM Error for token {token[:10]}... : {e}")

    return success_count > 0