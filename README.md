# PID-Simulation

PID-Simulation is a simple Python-based simulation of a Proportional-Integral-Derivative (PID) controller. It is a general-purpose simulation tool that can be used to visualize how a PID controller stabilizes rockets by plotting the system's response (rocket angle & nozzle angle over time).

## Prerequisites

- Python 3
- Pip 3
- Tkinter

## Installation

1. Clone this repository: `git clone https://github.com/FeliNUx42/PID-Simulation.git`
2. Go to the directory: `cd PID-Simulation/`
3. Install the required dependencies: `pip3 install -r requirements.txt`

## Usage

To run the simulation, simply execute the `main.py` script:

```bash
python3 main.py
```

The simulation will open a graphical user interface where you can enter the PID controller parameters (proportional, integral, and derivative gains), as well as the simulation duration, and a lot more stuff. Once you have entered these values, the simulation will run and display an animation and a plot of the system response.

## Examples

[Here](https://raw.githubusercontent.com/FeliNUx42/PID-Simulation/master/media/demo.mp4) is an example of how to run the simulation.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Contributing

If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Future Work

Some potential areas for future development include:

- Implementig better physics system, i.e include air resistance & maximum speed at which the nozzle can rotate
- Incorporating noise or disturbances into the simulation to test the system's robustness