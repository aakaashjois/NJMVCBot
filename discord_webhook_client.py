import os

from discord import Webhook, RequestsWebhookAdapter


class DiscordWebhookClient:
    def __init__(self, silent: bool = True):
        self.webhook = Webhook.partial(
            id=int(os.environ['DISCORD_WEBHOOK_ID']),
            token=os.environ['DISCORD_WEBHOOK_TOKEN'],
            adapter=RequestsWebhookAdapter(),
        )
        if not silent:
            self.send_message("Webhook client initialized")

    def send_message(self, message: str):
        self.webhook.send(content=message)


if __name__ == "__main__":
    client = DiscordWebhookClient(silent=False)
