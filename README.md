# Reinforcement Learning for Minecraft Parkour

Louis Caubet, Firas Ben Jedidia, Long Van Tran Ha, Léo Feliers, Inès Vignal <br>
2023 Project for the INF581 Advanced Machine Learning course at Ecole Polytechnique.

## Installation instructions

We recommend using Python 3.9 or newer in a virtual environment to run this project.

- Install Java JDK 8 ([AdoptOpenJDK](https://adoptium.net/))

- Install MineRL 

    - using `pip install git+https://github.com/minerllabs/minerl`
    - OR, if you don't want to install more than needed:
      ```
      git clone https://github.com/minerllabs/minerl.git
      set READTHEDOCS=true
      pip install -e minerl
      ```
      Using the READTHEDOCS environment will not build Minecraft when installing MineRL, which we don't need anyway.

- Install other python dependencies:
```
pip install -r requirements.txt
```

- Install Malmo & MalmoEnv:

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
