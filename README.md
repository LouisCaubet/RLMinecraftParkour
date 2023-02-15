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

-   Install other python dependencies:

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
Example: `python src/test_parkour_env.py`.
