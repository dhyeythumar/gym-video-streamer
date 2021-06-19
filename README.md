# Gym Video Streamer

**<h3 align="center">A Video Streaming Wrapper for OpenAI's Gym Environments</h3>**

<h4 align="center">
Now you can Live Stream the Agent's learning behavior to Twitch/YouTube from Google Colab while training these Agents.
</h4>

<p align="center">
    <a href="https://colab.research.google.com/github/dhyeythumar/gym-video-streamer/blob/main/Streaming-Gym-Envs-from-Colab.ipynb">
      <img alt="colab link" src="https://colab.research.google.com/assets/colab-badge.svg" />
    </a>
</p>

## What’s In This Document

-   [Installation](#installation)
-   [Imports and Usage](#imports-and-usage)
-   [Setup for different type of Gym Envs](#setup-for-different-type-of-gym-envs)
-   [License](#license)

## Installation

```bash
!pip install gym-video-streamer
```

And if you already have `gym-video-streamer` then upgrade it by this command.

```bash
!pip install --upgrade gym-video-streamer
```

## Imports and Usage

```python
import gym
from gym_video_streamer import SetupVirtualDisplay
from gym_video_streamer import VideoStreamer  # Streaming Wrapper
```

-   Now Setup the Virtual Display (only required for Google Colab):

    ```python
    SetupVirtualDisplay()
    ```

-   Define your live stream information:

    ```python
    # stream_info dictionary should be in this format only
    stream_info = {
        "URL": "rtmp://live.twitch.tv/app/", # example of Twitch URL
        "secret": "--- secret here ---"
    }
    ```

-   Initialize the gym env and pass it to the custom wrapper:

    ```python
    # ---- {For Classic-control gym envs} ----
    env = VideoStreamer(gym.make("CartPole-v1"), stream_info)
    ```

    \*_If you don't pass `stream_info` then it will simply store the video locally in the `videos` directory._

-   Test the setup (running 100 episodes for testing):

    ```python
    try:
        observation = env.reset()
        i = 0
        while True:
            if i == 100:
                break

            env.render()  # important to call render method on env
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)

            if done:
                env.reset()
                i += 1
    except Exception as e:
        print(e)
    finally:
        env.close()
    ```

## Setup for different type of Gym Envs

-   **`Classic control Gym Envs`**: As we have seen in the above example this type of works without any extra installation/setup.

-   **`Box2D Gym Envs`**: For this type of envs you need to install the following packages:

    ```bash
    !pip install box2d box2d-py
    ```

-   **`Atari Gym Envs`**: Using this type of envs on Google Colab you, need some extra setup to make them working. When I tried, it gave me the following error `Exception: ROM is missing for breakout, see https://github.com/openai/atari-py#roms for instructions`. So if you know how to setup this env on Colab then do let me know ✌🏻.

-   **`MuJoCo & Robotics Gym Envs`**: Now for this type of envs, you need to setup the MuJoCo on Colab. And again I haven't done this but I found a resource that will help you [Setup Mujoco-py on Linux](https://github.com/reinforcement-learning-kr/pg_travel/wiki/Installing-Mujoco-py-on-Linux).

## License

Licensed under the [MIT License](./LICENSE).
