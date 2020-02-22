# td-mirobot

#### [TouchDesigner](https://www.derivative.ca) version 2019.20140

License: MIT

[Matthew Wachter](https://www.matthewwachter.com)

[VT Pro Design](https://www.vtprodesign.com)

## Description

**td-mirobot** is a component that can be used to control the [WLkata}(www.wlkata.com/site/index.html) Mirobot

This component uses the G code protocol to communicate with the Mirobot over a serial connection. The official **G code instruction set** and **driver download** can be found on [HERE](http://www.wlkata.com/site/downloads.html)

## How to use
After installing the driver and powering the robot on, check in the Windows Device Manager under Ports to see which com port the Mirobot is attached to.

Open the TouchDesigner scene and type the corresponding com port into the Com parameter of the Mirobot component (e.g. com10). Toggle the Active switch to the On position. You should see the Mirobot respond with it's current position.

Always perform the homing routine after the Mirobot has been powered on. Completing the routine will automatically unlock the motors.

Once the Mirobot has completed its homing routine and the shaft has unlocked, it can be sent to specific positions using the promoted extension methods.

- Go to axis position:
	```
	op('mirobot').GoToAxis(90.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2000)
	```

- Go to Cartesian position:
	```
	op('mirobot').GoToCartesianLin(0.0, 0.0, 200.0, 0.0, 0.0, 0.0, 2000)
	```

## Parameters

#### Settings

- **Active** - Toggles the state of the serial connection.

- **Port** - Specifies the com port on which to connect to the Mirobot (can be found in the Windows Device Manager).

- **Homing Simultaneous** - Performs the homing routine on all axes simultaneously.

- **Homing Individual** - Performs the homing routine on all axes one at a time.

- **Unlock Shaft** - Unlocks the motors. Performing the homing routine also unlocks the motors so typically this button would not need to be used.

- **Go To Zero** - Sends each axis to its 0 position.

- **Air On** - Turns on the pneumatic air if the module is connected.

- **Air Off** - Turns off the pneumatic air if the module is connected.

- **Gripper On** - Closes the gripper if the module is connected.

- **Gripper Off** - Opens the gripper if the module is connected.

## Promoted Extension Methods

- **HomingSimultaneous()** - Performs the homing routine on all axes simultaneously.

- **HomingIndividual()** - Performs the homing routine on all axes one at a time.

- **SetHardLimit(state)** - Sets the hard limit state (True by default). Careful with this one!
	- **state (bool)** - The state to be set.

- **SetSoftLimit(state)** - Sets the soft limit state (True by default). Careful with this one!
	- **state (bool)** - The state to be set.

- **UnlockShaft()** - Unlocks the shaft enabling movement.

- **GoToZero()** - Sends each axis to its 0 position.

- **GoToAxis(a1, a2, a3, a4, a5, a6, speed)** - Send each axis to a specific position.
	- **a1 (float)** - Angle of axis 1.
	- **a2 (float)** - Angle of axis 2.
	- **a3 (float)** - Angle of axis 3.
	- **a4 (float)** - Angle of axis 4.
	- **a5 (float)** - Angle of axis 5.
	- **a6 (float)** - Angle of axis 6.
	- **speed (int)** - The velocity of the move.

- **IncrementAxis(a1, a2, a3, a4, a5, a6, speed)** - Increment each axis a specific amount.
	- **a1 (float)** - Angle increment of axis 1.
	- **a2 (float)** - Angle increment of axis 2.
	- **a3 (float)** - Angle increment of axis 3.
	- **a4 (float)** - Angle increment of axis 4.
	- **a5 (float)** - Angle increment of axis 5.
	- **a6 (float)** - Angle increment of axis 6.
	- **speed (int)** - The velocity of the move.

- **GoToCartesianPTP(x, y, z, a, b, c, speed)** - Point to point move to a Cartesian position.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **GoToCartesianLin(x, y, z, a, b, c, speed)** - Linear move to a Cartesian position.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **IncrementCartesianPTP(x, y, z, a, b, c, speed)** - Point to point increment in Cartesian space.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **IncrementCartesianLin(x, y, z, a, b, c, speed)** - Linear increment in Cartesian space.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **SetAirPump(pwm)** - Set the pwm of the pneumatic air pump.
	- **pwm** - The pulse width modulation frequency of the pneumatic air pump.

- **SetGripper(pwm)** - Set the pwm of the gripper.
	- **pwm** - The pulse width modulation frequency of the gripper.