#!/usr/bin/env python
import manager
import random
from openrocketdoc import document


# Build a rocket
# Nosecone
nose = document.Nosecone(
    document.Noseshape.TANGENT_OGIVE,  # Shape
    1.0,            # shape_parameter
    3.5,            # mass [kg]
    1.0,            # length [m]
    diameter=0.2,   # diameter [m] ~8 inches
)

# Payload section
payload = document.Bodytube(
    "Payload",      # Name
    3.5,            # mass [kg]
    0.33,           # length [m]
    diameter=0.2,   # diameter [m] ~8 inches
)

# Body section
body = document.Bodytube(
    "Body",         # Name
    10.0,           # mass
    2.0,            # length [m]
    diameter=0.2,   # diameter [m] ~8 inches
)

def rocket():

    # parametric thrust curve:
    peak_thrust = random.uniform(500, 2500)
    delay_time = random.uniform(0.5, 8.0)
    min_thrust = random.uniform(0.15, 0.9)
    growth_rate = random.uniform(1.01, 2.0)

    engine = document.Engine("Motor")
    engine.m_prop = 10.0 # kg
    engine.diameter = 0.2
    engine.length = 1.5

    isp = 200
    max_impulse = engine.m_prop * isp * 9.8

    thrust = 1.0
    thrustcurve = []
    itot = 0
    for i in range(500):
        t = i*0.1

        if t > delay_time:
            thrust = min_thrust * growth_rate**(t - delay_time)
            if thrust > 1.0:
                thrust = 1.0


        thrust_N = thrust * peak_thrust

        # compute Total impulse
        if i > 0:
            x = thrustcurve[-1]['t']
            x_1 = t
            f_x = thrustcurve[-1]['thrust']
            f_x1 = thrust_N
            itot += ((x_1 - x) * (f_x1 + f_x)) / 2.0

        thrustcurve.append({'t': t, 'thrust': thrust_N})

        # When we exceed our impulse budget quit
        if itot > max_impulse:
            break

    engine.thrustcurve = thrustcurve

    body.components = [engine]

    # Rocket:
    rocket = document.Rocket("Rocket")
    rocket.aero_properties['CD'] = [
        (0.010,0.699865),
        (0.200,0.580362),
        (0.300,0.586504),
        (0.400,0.595115),
        (0.500,0.606208),
        (0.600,0.619801),
        (0.700,0.635912),
        (0.800,0.654567),
        (0.900,0.675792),
        (0.950,0.681607),
        (1.000,0.688266),
        (1.050,0.725044),
        (1.100,0.722610),
        (1.200,0.657679),
        (1.300,0.595412),
        (1.400,0.572275),
        (1.500,0.550839),
        (1.600,0.530843),
        (1.700,0.512105),
        (1.800,0.494492),
        (1.900,0.477901),
        (2.000,0.462252),
    ]
    stage0 = document.Stage("Sustainer")
    stage0.components = [nose, payload, body]
    rocket.stages = [stage0]

    return rocket

#print(rocket())
manager.run(rocket, number_of_sims=5000, number_of_threads=4)
