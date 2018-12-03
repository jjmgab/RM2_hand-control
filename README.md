# Hand prosthetics control using Py3
*Course: Roboty Mobilne 2*

A project in Python3 utilizing tools such as:
  - Sympy
  - marshal
  
A goal is to implement inverse kinematics algorithm in order to create simple hand prosthetics control.

Script *hand_model.py* calculates matrices defining the hand model (relations between joints in D-H notation).
Script *finger_coordinates.py* substitutes for constants in the model (eg. lengths) 

To substitute for joint angle values, script *script.py* is used. To run and visualize results:

```
python3 script.py; cd gnuplot; python3 pyrunner.py
```
