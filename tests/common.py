import sys
import time

import gi

gi.require_version("Gst", "1.0")
from gi.repository import GLib, Gst


def test_main(pipeline):
    if isinstance(pipeline, str):
        pipeline = Gst.parse_launch(pipeline)
    loop = GLib.MainLoop()
    start_time = time.time()
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
        pass
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("<Ctrl + C> pressed")
    finally:
        pipeline.set_state(Gst.State.NULL)
        loop.quit()
        print(f"--- Ran for {time.time() - start_time:.3f} seconds")


if __name__ == "__main__":
    print("This module is not meant to be run directly.\n")
    sys.exit(-1)
