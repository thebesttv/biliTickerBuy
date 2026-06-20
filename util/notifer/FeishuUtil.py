import requests

from util.notifer.Notifier import NotifierBase


class FeishuNotifier(NotifierBase):
    def __init__(
        self,
        webhook_url,
        title,
        content,
        interval_seconds=10,
        duration_minutes=10,
    ):
        super().__init__(title, content, interval_seconds, duration_minutes)
        self.webhook_url = str(webhook_url or "").strip()

    def send_message(self, title, message):
        if not self.webhook_url:
            raise ValueError("Feishu webhook URL is required")

        # Feishu text message only supports plain text in content.text.
        text = f"{title}\n{message}" if title else message
        response = requests.post(
            self.webhook_url,
            json={
                "msg_type": "text",
                "content": {
                    "text": text,
                },
            },
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        if data.get("code", 0) != 0:
            raise RuntimeError(f"Feishu push failed: {data}")
