#!/bin/bash
export ELM_DISPLAY=fb
export EVAS_FB_DEV=/dev/fb2
rage "v4l2:///dev/video0"
