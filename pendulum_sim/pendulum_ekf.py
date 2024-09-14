# library imports
import numpy as np

from pendulum_simulation import *


def pendulum_state_update(x_n, dt):

    x_n[0] = x_n[0] + x_n[1]*dt
    x_n[1] = x_n[1] - (g/L) * np.sin(x_n[0]) * dt

    return x_n

def pendulum_jacobian(x_n, dt):

    return np.array([[ 1.0, dt], [ -(g/L) * np.cos(x_n[0])[0] * dt, 1.0 ]])

def ekf_predict_t(x_n, P_n):

    # prediction
    x_prediction_n = pendulum_state_update(x_n, dt)

    # uncertainty propagation
    pendulum_jacobian_n = pendulum_jacobian(x_n, dt)

    P_n = pendulum_jacobian_n @ P_n @ np.transpose(pendulum_jacobian_n) + Q

    return x_prediction_n, P_n

def observation_jacobian(x_prediction_n):

    return np.array([ L * np.cos(x_prediction_n[0])[0], 0]).reshape(1, -1)

def ekf_update_t(x_prediction_n, P_n, z):

    observation_value = L * np.sin(x_prediction_n[0])
    observation_jacobian_n = observation_jacobian(x_prediction_n)

    # calculate kalman gain
    k_n = P_n @ np.transpose(observation_jacobian_n) @ np.linalg.inv( observation_jacobian_n @ P_n @ np.transpose(observation_jacobian_n) + measurement_noise_std )

    # estimate state
    x_n = x_prediction_n + k_n * ( z - observation_value )

    # update estimate covariance
    P_n = ( np.eye(2) - k_n @ observation_jacobian_n ) @ P_n @ np.transpose( ( np.eye(2) - k_n @ observation_jacobian_n ) ) + (k_n * measurement_noise_std) @ np.transpose(k_n)

    return x_n, P_n
