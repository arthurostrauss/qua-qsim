# Qua-Qsim
Qua-Qsim, short for QUA Quantum Simulator, is a versatile tool that compiles QUA programs into hardware-agnostic pulse languages and simulates them on a quantum system. QUA programs are specifically designed for the Quantum Orchestration Platform (QOP) by Quantum Machines, which is used to control quantum systems.
With Qua-Qsim, you can simulate these programs without the need for a physical quantum computer, providing users with valuable insights and intuition about QUA and quantum computing in general.

Qua-Qsim currently features a compiler backend for Qiskit Pulse, allowing many QUA programs to be simulated using qiskit-dynamics. At present, we support fixed-frequency transmon qubits, and are actively working to expand support to include more qubit types and pulse languages. This ensures a broad range of applications and enhances the flexibility and utility of Qua-Qsim for various quantum computing projects.


## Installation
To start using Qua-Qsim, simply install it via pip:
```sh
pip install git+http://github.com/qua-platform/qua-qsim.git
```

## Example: Power Rabi
In this example, we demonstrate how to use Qua-Qsim to simulate simultaneous, two-qubit Rabi oscillations by performing an amplitude sweep on a simulated backend. Rabi oscillations are a fundamental phenomenon in quantum mechanics, representing the coherent oscillation of a qubit's state under the influence of an external driving field. This example will guide you through configuring a QUA program, defining the necessary parameters, and running the simulation to observe the resulting oscillations.

By following this example, you will gain hands-on experience with Qua-Qsim, learning how to set up and execute simulations that mimic real quantum experiments. This practical exercise will help solidify your understanding of both the QUA programming language and the underlying quantum principles.

### 0. Start with a QUA config

The first step in simulating a quantum experiment with Qua-Qsim is to create a QUA configuration. This configuration defines the hardware setup, including qubit parameters, control signals, and readout settings. In this example, we'll set up a configuration for two qubits and their associated resonators, specifying details such as intermediate frequencies, LO frequencies, pulse amplitudes, and lengths. More information can be found at [QUA Configuration](https://docs.quantum-machines.co/1.1.7/qm-qua-sdk/docs/Introduction/config/).

Creating an accurate QUA configuration is crucial as it ensures that the simulated environment closely mirrors the behavior of a real quantum system. Below is an example QUA configuration for our Power Rabi simulation:

<details> 
  <summary>Example QUA config</summary>

```python

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

x90_q1_amp = 0.08
x90_q2_amp = 0.068

x90_len = 260 // 4

qubit_1_IF = 50 * u.MHz
qubit_1_LO = 4860000000 - qubit_1_IF

qubit_2_IF = 60 * u.MHz
qubit_2_LO = 4970000000 - qubit_2_IF

resonator_1_LO = 5.5 * u.GHz
resonator_1_IF = 60 * u.MHz

resonator_2_LO = 5.5 * u.GHz
resonator_2_IF = 60 * u.MHz

readout_len = 5000
readout_amp = 0.2

time_of_flight = 24

config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                1: {"offset": 0.0},  # I resonator 1
                2: {"offset": 0.0},  # Q resonator 1
                3: {"offset": 0.0},  # I resonator 2
                4: {"offset": 0.0},  # Q resonator 2
                5: {"offset": 0.0},  # I qubit 1
                6: {"offset": 0.0},  # Q qubit 1
                7: {"offset": 0.0},  # I qubit 2
                8: {"offset": 0.0},  # Q qubit 2
            },
            "digital_outputs": {},
            "analog_inputs": {
                1: {"offset": 0.0, "gain_db": 0},  # I from down-conversion
                2: {"offset": 0.0, "gain_db": 0},  # Q from down-conversion
            },
        },
    },
    "elements": {
        "qubit_1": {
            "RF_inputs": {"port": ("octave1", 3)},
            "intermediate_frequency": qubit_1_IF,
            "operations": {
                "x90": "x90_q1_pulse",
                "y90": "y90_q1_pulse",
            },
        },
        "qubit_1t2": {
            "RF_inputs": {"port": ("octave1", 3)},
            "intermediate_frequency": qubit_2_IF,
            "operations": {
                "x90": "x90_pulse",
            },
        },
        "qubit_2": {
            "RF_inputs": {"port": ("octave1", 4)},
            "intermediate_frequency": qubit_2_IF,
            "operations": {
                "x90": "x90_q2_pulse",
            },
        },
        "resonator_1": {
            "RF_inputs": {"port": ("octave1", 1)},
            "RF_outputs": {"port": ("octave1", 1)},
            "intermediate_frequency": resonator_1_IF,
            "operations": {
                "readout": "readout_pulse",
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "resonator_2": {
            "RF_inputs": {"port": ("octave1", 2)},
            "RF_outputs": {"port": ("octave1", 1)},
            "intermediate_frequency": resonator_2_IF,
            "operations": {
                "readout": "readout_pulse",
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
    },
    "octaves": {
        "octave1": {
            "RF_outputs": {
                1: {
                    "LO_frequency": resonator_1_LO,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 0,
                },
                2: {
                    "LO_frequency": resonator_2_LO,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 0,
                },
                3: {
                    "LO_frequency": qubit_1_LO,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 0,
                },
                4: {
                    "LO_frequency": qubit_2_LO,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 0,
                },
            },
            "RF_inputs": {
                1: {
                    "LO_frequency": resonator_1_LO,
                    "LO_source": "internal",
                },
            },
            "connectivity": "con1",
        }
    },
    "pulses": {
        "x90_q1_pulse": {
            "operation": "control",
            "length": x90_len,
            "waveforms": {
                "I": "x90_q1_I_wf",
                "Q": "x90_q1_Q_wf",
            },
        },
        "y90_q1_pulse": {
            "operation": "control",
            "length": x90_len,
            "waveforms": {
                "I": "y90_q1_I_wf",
                "Q": "y90_q1_Q_wf",
            },
        },
        "x90_q2_pulse": {
            "operation": "control",
            "length": x90_len,
            "waveforms": {
                "I": "x90_q2_I_wf",
                "Q": "x90_q2_Q_wf",
            },
        },
        "y90_q2_pulse": {
            "operation": "control",
            "length": x90_len,
            "waveforms": {
                "I": "y90_q2_I_wf",
                "Q": "y90_q2_Q_wf",
            },
        },
        "readout_pulse": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
            },
            "digital_marker": "ON",
        },
    },
    "waveforms": {
        "zero_wf": {"type": "constant", "sample": 0.0},
        # q1
        "x90_q1_I_wf": {"type": "constant", "sample": x90_q1_amp},
        "x90_q1_Q_wf": {"type": "constant", "sample": 0.},
        "y90_q1_I_wf": {"type": "constant", "sample": 0.},
        "y90_q1_Q_wf": {"type": "constant", "sample": x90_q1_amp},
        # q2
        "x90_q2_I_wf": {"type": "constant", "sample": x90_q2_amp},
        "x90_q2_Q_wf": {"type": "constant", "sample": 0.},
        "y90_q2_I_wf": {"type": "constant", "sample": 0.},
        "y90_q2_Q_wf": {"type": "constant", "sample": x90_q2_amp},
        "readout_wf": {"type": "constant", "sample": readout_amp},
    },
    "digital_waveforms": {
        "ON": {"samples": [(1, 0)]},
    },
}


```
</details>

### 1. Define your simulated quantum parameters

With the QUA configuration in place, the next step is to define the parameters for your simulated quantum system. These parameters include the physical characteristics of the qubits and their interactions within the simulation environment. In this example, we will specify the parameters for a system of two fixed-frequency transmon qubits.

Below is an example of how to define the quantum parameters for our simulation:

```python
from quaqsim.architectures.transmon_pair import TransmonPair
from quaqsim.architectures import TransmonSettings
from quaqsim.architectures.transmon_pair_settings import TransmonPairSettings

settings = TransmonPairSettings(
    TransmonSettings(
        resonant_frequency=4860000000.0,
        anharmonicity=-320000000.0,
        rabi_frequency=0.22e9
    ),
    TransmonSettings(
        resonant_frequency=4970000000.0,
        anharmonicity=-320000000.0,
        rabi_frequency=0.26e9
    ),
    coupling_strength=0.002e9
)

transmon_pair = TransmonPair(settings)
```


### 2. Map your QUA elements to simulation channels

After defining your simulated quantum parameters, the next step is to map the elements from your QUA configuration to the corresponding simulation channels. This mapping ensures that the quantum operations defined in your QUA program are correctly applied to the simulated qubits and resonators.

Mapping QUA elements to simulation channels involves linking each element in your QUA configuration to the appropriate backend channel in your simulation setup. This step is crucial for accurate simulation, as it aligns the logical operations in your QUA program with the physical actions in the simulated quantum system.

Below is an example of how to map QUA elements to simulation channels:

```python
from quaqsim.architectures.from_qua_channels import (
    TransmonPairBackendChannelReadout,
    TransmonPairBackendChannelIQ, 
    ChannelType
)

qubit_1_freq = 4860000000
qubit_2_freq = 4970000000.0

channel_map = {
    "qubit_1": TransmonPairBackendChannelIQ(
        qubit_index=0,
        carrier_frequency=qubit_1_freq,
        operator_i=transmon_pair.transmon_1_drive_operator(quadrature='I'),
        operator_q=transmon_pair.transmon_1_drive_operator(quadrature='Q'),
        type=ChannelType.DRIVE
    ),
    "qubit_1t2": TransmonPairBackendChannelIQ(
        qubit_index=0,
        carrier_frequency=qubit_2_freq,
        operator_i=transmon_pair.transmon_1_drive_operator(quadrature='I'),
        operator_q=transmon_pair.transmon_1_drive_operator(quadrature='Q'),
        type=ChannelType.CONTROL
    ),
    "qubit_2": TransmonPairBackendChannelIQ(
        qubit_index=1,
        carrier_frequency=qubit_2_freq,
        operator_i=transmon_pair.transmon_2_drive_operator(quadrature='I'),
        operator_q=transmon_pair.transmon_2_drive_operator(quadrature='Q'),
        type=ChannelType.DRIVE
    ),
    "resonator_1": TransmonPairBackendChannelReadout(0),
    "resonator_2": TransmonPairBackendChannelReadout(1),
}
```

In this example, we link each QUA element, such as qubit_1 and resonator_1, to their corresponding backend channels. This mapping ensures that the operations defined in your QUA program, like driving a qubit or reading out a resonator, are accurately reflected in the simulation.

By completing this step, you establish a direct correspondence between the high-level QUA elements and the low-level simulation channels, enabling precise control and measurement within the simulated quantum environment.

### 3. Define a QUA Program

With the configuration and mappings set up, the next step is to define your QUA program. This program specifies the quantum operations you want to perform, such as driving qubits and measuring their states.

Below is an example of a QUA program for simulating Rabi oscillations with an amplitude sweep:

```python
from qm.qua import *

start, stop, step = -2, 2, 0.1
with program() as prog:
    a = declare(fixed)

    with for_(a, start, a < stop - 0.0001, a + step):
        play("x90"*amp(a), "qubit_1")
        play("x90"*amp(a), "qubit_2")

        align("qubit_1", "qubit_2", "resonator_1", "resonator_2")
        measure("readout", "resonator_1", None)
        measure("readout", "resonator_2", None)

```

In this program, we perform an amplitude sweep on two qubits, playing x90 pulses and measuring the readout from the resonators. This setup allows us to observe the Rabi oscillations in the simulation.

### 4. Simulate!

The final step is to run the simulation and visualize the results. This involves using Qua-Qsim to simulate the QUA program and then plotting the resulting data to observe the Rabi oscillations.

```python
import numpy as np
import matplotlib.pyplot as plt

from quaqsim import simulate_program
from quaqsim.architectures.transmon_pair_backend_from_qua import \
    TransmonPairBackendFromQUA

backend = TransmonPairBackendFromQUA(transmon_pair, channel_map)

results = simulate_program(
    qua_program=prog,
    qua_config=config,
    qua_config_to_backend_map=channel_map,
    backend=backend,
    num_shots=10_000,
)

for i, result in enumerate(results):
    plt.plot(np.arange(start, stop, step), results[i], '.-', label=f"Simulated Q{i}")
    plt.ylim(-0.05, 1.05)
plt.legend()
plt.show()
```

In this example, we use the simulate_program function to run the QUA program on the defined backend, then plot the simulation results to visualize the Rabi oscillations for each qubit.

**Result**
![](img/rabi_example.png)