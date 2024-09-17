from utils import http_publisher, subscriber
async def start():
    await subscriber.run()
    http_publisher.run()