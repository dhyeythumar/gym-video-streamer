# author:	Dhyey Thumar
# website:	https://github.com/dhyeythumar/gym-video-streamer

# set the version number
__version__ = "1.0"

from .setupVirtualDisplay import SetupVirtualDisplay
from .gymVideoStreamingWrapper import VideoStreamingWrapper as VideoStreamer

# --- Note on versioning ---
# Only minor changes & patches should be released under v1.0 as v1.0.0, v1.0.1, v1.0.2...

# v1.1.0 & v1.1.1 won't work as they are already used because of my silliness 😥.
# So just use v2.x.x
