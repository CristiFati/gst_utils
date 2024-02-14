#!/usr/bin/env python

import sys
import time

import gi

from tests.common import test_main
from gst_utils.pipeline_parser import PipelineParser

gi.require_version("Gst", "1.0")
from gi.repository import GLib, Gst


def create_dummy_pipeline():
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
        return

    pipeline = Gst.Pipeline()
    if not pipeline:
        print("No pipeline")
        return

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
        return
    return pipeline


def main(*argv):
    Gst.init(None)
    pipeline = create_dummy_pipeline()
    if not pipeline:
        return -1
    test_main(pipeline)
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

