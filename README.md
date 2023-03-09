# Reinforcement Learning for Minecraft Parkour

Louis Caubet, Firas Ben Jedidia, Long Van Tran Ha, Léo Feliers, Inès Vignal <br>
2023 Project for the INF581 Advanced Machine Learning course at Ecole Polytechnique.

## Installation instructions

We recommend using Python 3.9 in a virtual environment to run this project.

-   Install Java JDK 8 ([AdoptOpenJDK](https://adoptium.net/))

-   Clone this repository:

```
git clone https://github.com/LouisCaubet/RLMinecraftParkour.git

cd RLMinecraftParkour
```

-   Install python dependencies:

```
pip install -r requirements.txt
```

-   Install Malmo & MalmoEnv:

```
git clone https://github.com/Microsoft/malmo.git

cd malmo/Minecraft

(echo -n "malmomod.version=" && cat ../VERSION) > ./src/main/resources/version.properties
```

## Running the code

Start Minecraft with Malmo in a terminal by running

```
cd malmo/Minecraft
launchClient.bat -port 9000 -env
```

Open another terminal to run our code.

You can then run the desired Python script. Make sure it is executed from the root of the project.

-   `python src/test_parkour_env.py` will simply open the `parkour_env` in Minecraft.
-   `python src/sb3_training.py` will run the training using Stable-Baselines3
-   `python src/sb3_testing.py` will run the SB3 trained model in inference mode.

## Configuration

Use the `.env` file for configuration. Here's a list of environment variables we use:

-   `MINERL_PARKOUR_MAP`: Path to the CSV defining the map.
-   `MALMO_PORT`: Port on which Malmo is running (default: 9000)
-   `SB3_ALGO`: Algorithm to use for training. Possible values: DQN, PPO, A2C
-   `SB3_TIMESTEPS`: Number of training timesteps
-   `S3_TRAINED_MODEL_NAME`: Name under which to save the model after training.
-   `SB3_INFERENCE_MODEL_NAME`: Model to use for inference in the `sb3_predict` script.
-   `SB3_INFERENCE_STEPS`: Number of steps to run inference for.

## Results

### Level 1: Straight line, easy first level to test setup

Trained using PPO with 10k steps.

Action space: _Move, Strafe_

Rewards:

-   +100 for reaching the diamond block
-   +10 for each (gold) block towards the goal
-   -100 and end of episode when touching the bedrock

https://user-images.githubusercontent.com/59528773/220745121-85449269-235f-4d0d-a1b3-a1aea2f5c0fa.mp4

### Level 2: Narrower straight line with one-block jump

Action space: _Move, Strafe_, _JumpStrafe_

Rewards:

-   +100 for reaching the diamond block
-   +10 for each (gold) block towards the goal
-   -100 and end of episode when touching the bedrock

When training using PPO with 10k timesteps, **the agent hacks the game!** (Manages to jump for way longer distances that it should be possible)

_video_

To prevent this, add a minimum delay of 0.1s between actions. To adapt the agent to this new environment, we finetune the previous model for 2k more timesteps. Now, it works!

_video_

_Note: Due to the time.sleep, sometimes the +100 reward is not given despite the agent being on the diamond block._
