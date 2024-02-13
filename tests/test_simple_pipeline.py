#!/usr/bin/env python

import sys
import time

import gi

from gst_utils.pipeline_parser import PipelineParser

gi.require_version("Gst", "1.0")
from gi.repository import GLib, Gst


def create_pipeline(pipeline):
    elements = []
    videotest0 = Gst.ElementFactory.make("videotestsrc")
    videotest0.set_property("pattern", 18)
    elements.append(videotest0)
    capsfilter0 = Gst.ElementFactory.make("capsfilter")
    capsfilter0.set_property("caps", Gst.Caps.from_string("video/x-raw,format=NV12"))
    elements.append(capsfilter0)
    tee0 = Gst.ElementFactory.make("tee")
    elements.append(tee0)
    queue0 = Gst.ElementFactory.make("queue")
    elements.append(queue0)
    avsink0 = Gst.ElementFactory.make("autovideosink")
    avsink0.set_property("sync", 0)
    elements.append(avsink0)
    queue1 = Gst.ElementFactory.make("queue")
    elements.append(queue1)
    fakesink0 = Gst.ElementFactory.make("fakesink")
    fakesink0.set_property("sync", 0)
    elements.append(fakesink0)

    if not all(elements):
        print("Elements not created: ", end="")
        for i, e in enumerate(elements):
            if not e:
                print(i, end=", ")
        print()
        return False
    for e in elements:
        pipeline.add(e)

    links = (
        videotest0.link(capsfilter0),
        capsfilter0.link(tee0),
        tee0.link(queue0),
        queue0.link(avsink0),
        tee0.link(queue1),
        queue1.link(fakesink0),
    )
    if not all(links):
        print(f"Link failures: {links}")
        return False
    return True


def main(*argv):
    Gst.init(None)
    pipeline = Gst.Pipeline()
    if not pipeline:
        print("No pipeline")
        return -1
    res = create_pipeline(pipeline)
    if not res:
        print("No pipeline elements")
        return -1
    start_time = time.time()
    loop = GLib.MainLoop()
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

    pp = PipelineParser()
    print(f"\nGST Launch equivalent:\n{pp.gst_launch(pipeline)}")


if __name__ == "__main__":
    print(
        "Python {:s} {:03d}bit on {:s}\n".format(
            " ".join(elem.strip() for elem in sys.version.split("\n")),
            64 if sys.maxsize > 0x100000000 else 32,
            sys.platform,
        )
    )
    rc = main(*sys.argv[1:])
    print("\nDone.\n")
    sys.exit(rc)

