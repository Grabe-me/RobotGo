import asyncio
import logging

from robotgo.api_servers.server import serve

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.get_event_loop().run_until_complete(serve())
    except KeyboardInterrupt:
        logging.info("shutdown server")
        exit()
