#!/bin/bash
cd /tmp/
socat tcp-l:42069,reuseaddr,fork EXEC:"/chal/run.sh",pty,stderr
