#!/bin/bash
export ELM_DISPLAY=fb
export EVAS_FB_DEV=/dev/fb2
terminology -e 'su simon -c "cvlc v4l2:///dev/video0"'
