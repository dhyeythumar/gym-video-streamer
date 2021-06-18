from gym import error
import distutils.spawn
import distutils.version
import numpy as np
import subprocess
import os
from datetime import datetime


def printMsg(feedbackMsg, errMsg=""):
    print("="*200)
    print(feedbackMsg)
    if errMsg != "":
        print("-"*100)
        print(errMsg)
    print("="*200)


def touch(path):
    open(path, 'a').close()


class Streamer(object):
    def __init__(self, frame_shape, frames_per_sec, output_frames_per_sec, streamURL):
        self.proc = None
        # Frame shape should be lines-first, so w and h are swapped
        h, w, pixfmt = frame_shape
        if pixfmt != 3 and pixfmt != 4:
            raise error.InvalidFrame(
                "Your frame has shape {}, but we require (w,h,3) or (w,h,4), i.e., \
                RGB values for a w-by-h image, with an optional alpha channel.".format(frame_shape))

        self.wh = (w, h)
        self.includes_alpha = (pixfmt == 4)
        self.frame_shape = frame_shape
        self.frames_per_sec = frames_per_sec
        self.output_frames_per_sec = output_frames_per_sec
        self.ffmpegOutput = ""

        # this it will stream
        if streamURL != "":
            self.ffmpegOutput = streamURL
        # if not possible then record the video & save it locally
        else:
            directory = "./videos"
            if not os.path.exists(directory):
                print("Creating directory for storing videos {%s}", directory)
                os.makedirs(directory, exist_ok=True)

            self.__directory = os.path.abspath(directory)
            date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
            self.ffmpegOutput = os.path.join(self.__directory, '{}'.format(date))
            touch(self.ffmpegOutput)  # just in case

        if distutils.spawn.find_executable("ffmpeg") is not None:
            self.backend = "ffmpeg"
        else:
            raise error.DependencyNotInstalled("No ffmpeg executable found!")
        self.start()

    def start(self):
        self.cmdline = [self.backend,
                        "-nostats",
                        "-loglevel", "error",  # suppress warnings
                        '-y',
                        "-threads:v", "4",
                        "-filter_threads", "4",

                        # input
                        "-f", "rawvideo",
                        "-s:v", "{}x{}".format(*self.wh),  # size of one frame
                        "-pix_fmt", ("rgb32" if self.includes_alpha else "rgb24"),
                        "-framerate", "%d" % self.frames_per_sec,
                        "-i", "-",  # The input comes from a pipe

                        "-b:v", "600k",  # bitrate
                        # "-minrate:v", "600k",
                        # "-maxrate:v", "600k",
                        # "-bufsize:v", "600k",

                        # output
                        "-vcodec", "libx264",
                        "-pix_fmt", "yuv420p",
                        "-r:v", "%d" % self.output_frames_per_sec,

                        "-crf", "18",  # lower CRF values correspond to higher bitrates,
                        "-bf:v", "3",  # set maximum number of B frames between non-B-frames
                        "-refs:v", "16",  # reference frames to consider for motion compensation
                        "-f", "flv",
                        self.ffmpegOutput
                        ]
        self.proc = subprocess.Popen(self.cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def capture_frame(self, frame):
        if not isinstance(frame, (np.ndarray, np.generic)):
            raise error.InvalidFrame('Wrong type {} for {} (must be np.ndarray or np.generic)'.format(type(frame), frame))
        if frame.shape != self.frame_shape:
            raise error.InvalidFrame("Your frame has shape {}, but the VideoRecorder is configured for shape {}.".format(frame.shape, self.frame_shape))
        if frame.dtype != np.uint8:
            raise error.InvalidFrame("Your frame has data type {}, but we require uint8 (i.e. RGB values from 0-255).".format(frame.dtype))

        # write this frame to the writable stream of subprocess
        out = self.proc.stdin.write(frame.tobytes())
        if out is None:
            raise error.Error("ffmpeg streaming broken & gave '{}' error".format(out))

    def close(self):
        self.proc.stdin.close()
        ret = self.proc.wait()
        if ret != 0:
            printMsg("Streamer encoder exited with status {}".format(ret))
