import app
import time
import traceback
import socket
import os

if __name__ == "__main__":
    exp_backoff = 0
    while True:
        try:
            _app = app.make_app(os.environ.get("JORRVASKR_CONFIG", "config.Config"))
            _app.run(host=os.environ.get("JORRVASKR_HOST", "0.0.0.0"))
        except (KeyboardInterrupt, SystemExit, socket.error):
            raise
        except Exception as e:
            traceback.print_exc()
            exp_backoff += 1
            retry_gap = 3 ** exp_backoff
            print("Retrying in %ss..." % retry_gap)
            time.sleep(retry_gap)
