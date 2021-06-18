import gym
from gym import error, Wrapper
from .streamer import printMsg, Streamer

STREAM_INFO_ERR_MSG = "The provided Stream Info dictionary is not correctly passed!\n\
Video won't be streamed. Instead it will be stored locally @ ./videos/"

class VideoStreamingWrapper(Wrapper):
    def __init__(self, env, streamInfo=None):
        super(VideoStreamingWrapper, self).__init__(env)
        self.Streamer = None
        self.frames_per_sec = env.metadata.get('video.frames_per_second', 30)
        self.output_frames_per_sec = env.metadata.get('video.output_frames_per_second', self.frames_per_sec)

        modes = env.metadata.get('render.modes', [])  # can be {'human', 'ansi', 'rgb_array'}
        self.enabled = True
        self.streamURL = ""

        if "rgb_array" not in modes:
            self.enabled = False
            printMsg("Disabling Video Streaming Wrapper because {} it doesn't supports 'rgb_array'.".format(env))
        else:
            try:
                if ((streamInfo is not None) and (streamInfo["URL"] != "") and (streamInfo["secret"] != "")):
                    self.streamURL = streamInfo["URL"] + streamInfo["secret"]
                    printMsg("Video Streaming Wrapper is ready to stream!!")
                else:
                    printMsg(STREAM_INFO_ERR_MSG)
            except Exception as e:
                printMsg(STREAM_INFO_ERR_MSG, e)

    def render(self, mode=None, **kwargs):
        # print(self.metadata)  # eg: {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 50}
        if self.enabled is True:
            frame = self.env.render(mode="rgb_array", **kwargs)
            try:
                if self.Streamer is None:
                    self.Streamer = Streamer(
                        frame.shape,
                        self.frames_per_sec,
                        self.output_frames_per_sec,
                        self.streamURL
                    )
                self.Streamer.capture_frame(frame)
                return True
            except (error.InvalidFrame,
                    error.DependencyNotInstalled,
                    error.Error) as e:
                self.enabled = False
                printMsg("Video Streaming Wrapper exited with an exception!", e)
                return self.env.render(mode, **kwargs)
        else:
            return self.env.render(mode, **kwargs)

    def close(self):
        super(VideoStreamingWrapper, self).close()
        if self.enabled is True:
            self.enabled = False
            if self.Streamer is not None:
                self.Streamer.close()
            else:
                printMsg("Environment closed before Video Streaming Wrapper could capture anything.")


# Test the VideoStreamingWrapper with simple CartPole Agent
if __name__ == "__main__":
    # No streamInfo provided then video will be stored locally
    env = VideoStreamingWrapper(gym.make("CartPole-v1"))
    # print(env.action_space)
    try:
        observation = env.reset()
        i = 0
        while True:
            if i == 100:
                break
            env.render()
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                env.reset()
                i += 1
    except Exception as e:
        print(e)
    finally:
        env.close()

# ---- References ----
# 1. https://github.com/openai/gym/blob/master/gym/wrappers/monitor.py
# 2. https://github.com/openai/gym/blob/master/gym/wrappers/monitoring/video_recorder.py
