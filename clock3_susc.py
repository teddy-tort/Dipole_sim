import numpy as np
from itertools import product
import matplotlib.pylab as plt
from ising_susc import calc_chi2

a = 1.1  # nm
a_cubed = a ** 3
p = 0.08789  # electron charge - nm
eps_rel = 1.5

eps0 = 0.0552713  # (electron charge)^2 / (eV - nm)
k_B = 8.617e-5  # eV / K
coupling_energy = p * p / (4 * np.pi * eps_rel * eps0 * a_cubed)


def calc_chi2_odd(T):
    beta = 1. / (k_B * T)
    return 9 * p * p * beta / (eps0 * a_cubed * (6 + 3 * np.exp(1.5 * coupling_energy * beta)))


def calc_chi2_even(T):
    beta = 1. / (k_B * T)
    argv = 1.5 * coupling_energy * beta
    return p * p * beta * (6 + 3 * np.exp(argv)) / (eps0 * a_cubed * (6 + 3 * np.exp(argv)))


def calc_chi(T: np.ndarray, N: int):
    """
    Calculate the electric susceptibility for a 1D ising model.
    :param T: Temperatures in Kelvin.
    :param N: Number of dipoles.
    :return: electric susceptibility
    """
    # volume = a_cubed * N
    Z_second_derivative = 0.
    Z_first_derivative = 0.
    Z = 0.
    beta = 1. / (k_B * T)
    for state in product(*[(1, 2, 3)] * N):
        s = np.array(state, dtype=np.float64)
        gamma = s[1:] - s[:-1]
        gamma[gamma != 0] = -0.5
        gamma[gamma == 0] = 1.
        s[s > 1] = -0.5
        sum_s = np.sum(s)
        sum_gamma = np.sum(gamma)
        prob_state = np.exp(-beta * coupling_energy * sum_gamma)
        Z_second_derivative += (sum_s * sum_s) * prob_state
        Z_first_derivative += sum_s * prob_state
        Z += prob_state
    return p * p * beta / (eps0 * a_cubed * Z) * (Z_second_derivative - Z_first_derivative * Z_first_derivative / Z)


def plot1():
    T_lim = 1000
    T = np.linspace(1, T_lim, 500)
    for nn in range(2, 15):
        plt.plot(T, calc_chi(T, nn), label=f"N={nn}")
    plt.ylim((0, 50))
    plt.xlim((0, T_lim))
    plt.legend()
    plt.show()


def plot_vs_ising():
    T_lim = 1000
    T = np.linspace(1, T_lim, 500)
    plt.plot(T, calc_chi(T, 2), label=f"calc")
    plt.plot(T, calc_chi2_even(T), label="exact")
    plt.plot(T, calc_chi2(2, T))
    plt.plot(T, calc_chi2_odd(T), label="exact")
    plt.plot(T, calc_chi2(-1, T))
    plt.ylim((0, 50))
    plt.xlim((0, T_lim))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot_vs_ising()
