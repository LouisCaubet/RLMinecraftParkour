# Reinforcement Learning for Minecraft Parkour

Louis Caubet, Firas Ben Jedidia, Long Van Tran Ha, Léo Feliers, Inès Vignal <br>
2023
<br>
Project for the INF581 Advanced Machine Learning course at Ecole Polytechnique.

## Setup

We recommend using Python 3.9 or newer in a virtual environment to run this project.

This project uses [MineRL](minerl.readthedocs.io/). Follow the instructions [here](https://minerl.readthedocs.io/en/latest/tutorials/index.html) to install this package.
We only use the `minerl.herobraine` module, so you can also just install that if the default minerl installation fails.

We use [MalmoEnv](https://github.com/microsoft/malmo/tree/master/MalmoEnv) to run the Minecraft environment.
Follow the instructions in the link to install.

Other requirements can be found in the `requirements.txt` file, which can be installed using `pip install -r requirements.txt`.

To check that your MineRL installation completed successfully, you can run the `test_minerl.py` script.

## Running the code

A Minecraft instance running MalmoEnv must be started separately.
Run `launchClient.bat -port 9000 -env` in the `malmo/Minecraft` folder to start the Minecraft client.

You can then run the desired Python script from our code. Make sure it is executed from the root of the project.
Example: `python src/test_parkour_env.py`.
