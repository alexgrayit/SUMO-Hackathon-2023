# SUMO Hackathon 2023

## Problem 1
### Definitions and Parameters
For this problem we define that the input file will be in the form
```
<N_laps>, <n_sensors>
<x_1>, <y_1>, <t_1>, <t_2>, ... , <t_N>
<x_2>, <y_2>, <t_1>, <t_2>, ... , <t_N>
.
.
.
<x_n>, <y_n>, <t_1>, <t_2>, ... , <t_N>
```
Where the first line defines the number of laps (measurements made by each sensor) each subsequent
line corresponds to sensor $n$ and has an $x$ and a $y$ coordinate for that sensor as its first two items,
and then the following $N$ items are the times at which the car passed that sensor (in chronological order).
The $x$, $y$ coordinates and $N_\text{laps}$ and $n_{\text{sensors}}$ are formatted as `int` and the times are `float`.

Here we make the specific assumption that all times will be rounded to 10 decimal places.