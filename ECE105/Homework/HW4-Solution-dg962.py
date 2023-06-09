import numpy as np
import matplotlib.pyplot as plt

"""
Daniel Goulding
14511512

ASSIGNMENT: COMPLETE functions plot_fsc(), plot_fse() below
"""

"""
ECE 105: Programming for Engineers 2
Created September 7, 2020
Steven Weber

Modified April 26, 2023
Naga Kandasamy

Fourier series error analysis starter code

This code plots the Fourier series representation, coefficients, and error of periodic signals
"""

# same as Lab 4
# Fourier series coefficient n for f using basis function b
def fsc(n, b, f, x, dx):
    # integral: (1/pi) f(xe) b(n xe) dx over all xe in x
    return np.sum([f(xe) * b(xe*n) for xe in x]) * dx / np.pi

# same as Lab 4
# compute Fourier series coefficients: a0, a, b
def fsc_all(N_max, f, x, dx):
    a0 = fsc(0, np.cos, f, x, dx)
    a = [fsc(n, np.cos, f, x, dx) for n in range(1,N_max+1)]
    b = [fsc(n, np.sin, f, x, dx) for n in range(1,N_max+1)]
    return a0, a, b

# same as Lab 4
# Fourier series representation at x using N terms
def fs(x, a0, a, b, N):
    # sum the a_n coefficients from 1 to N
    a_sum = np.sum([a[n-1] * np.cos(n * x) for n in range(1,N+1)], axis=0)
    # sum the b_n coefficients from 1 to N
    b_sum = np.sum([b[n-1] * np.sin(n * x) for n in range(1,N+1)], axis=0)
    # return the Fourier series approximation
    return a0/2 + a_sum + b_sum

# Fourier series error at x
def fse(x, f, a0, a, b, N):
    return np.abs(f(x) - fs(x, a0, a, b, N))

# same as Lab 4
# plot_fsr: 4 subplots: f(x) and Fourier series using N1, N2, N3 terms
def plot_fsr(f, N1, N2, N3, x, dx, name, filename):
    # get all Fourier series coefficients
    a0, a, b = fsc_all(max(N1,N2,N3), f, x, dx)
    plt.figure()
    ay,(ax1,ax2,ax3,ax4)=plt.subplots(nrows=4, sharex=True)
    plt.tight_layout()
    ax1.plot(x, f(x))
    ax2.plot(x, fs(x, a0, a, b, N1))
    ax3.plot(x, fs(x, a0, a, b, N2))
    ax4.plot(x, fs(x, a0, a, b, N3))
    ax1.set_title('{}: f(x)'.format(name))
    ax2.set_title('{}: Fourier series, N = {}'.format(name, N1))
    ax3.set_title('{}: Fourier series, N = {}'.format(name, N2))
    ax4.set_title('{}: Fourier series, N = {}'.format(name, N3))
    plt.savefig(filename)

"""
COMPLETE:
plot_fse plots the Fourier series representation error
Inputs:
1) f: the function to be approximated
2) N_max: maximum number of series terms
3) x: list of x-values from [-pi,+pi]
4) dx: width of each interval  in [-pi,+pi]
5) name: string describing f
6) filename: string for saving plot
Your code should do the following
1) get all the Fourier series coefficients a0, a, b from fsc_all
2) sum fse() over x to compute sum error for each N from 1,...N_max
3) use Matplotlib plt.bar to plot sum error vs. N from 1,...,N_max
* Make sure to add x-axis label, y-axis label, title, and save figure
"""
# Plot Fourier series error
def plot_fse(f, N_max, x, dx, name, filename):
    # 1. get all Fourier series coefficients
    a_0, a, b = fsc_all(N_max, f, x, dx)
    # ax = fig.subplots(111)
    # print(type(ax))
    # 2. call fse to compute the error for each xe in x, then sum
    error = [sum([fse(xe, f, a_0, a, b, N) for xe in x]) for N in range(0, N_max)]
    # 3. plot Fourier series representation error vs. N
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(range(0,N_max),error)
    ax.set_title(f"Error for {name}")
    plt.ylabel("Error")
    plt.xlabel("N")
    plt.savefig(filename)

"""
COMPLETE:
plot_fsc plots the Fourier series coefficients a_n, b_n
Inputs:
1) f: the function to be approximated
2) N_max: maximum number of series terms
3) x: list of x-values from [-pi,+pi]
4) dx: width of each interval  in [-pi,+pi]
5) name: string describing f
6) filename: string for saving plot
Your code should do the following
1) get all the Fourier series coefficients a0, a, b from fsc_all
2) insert a0 as first element in list a and 0 as first in list b
3) use Matplotlib plt.bar to make a plot with two subplots
* Top plot: plot of a_n vs. n for n = 0,...,N_max
* Bottom plot: plot of b_n vs. n for n = 0,...,N_max
* Make sure to add title to each subplot and save the figure
* Consider using plt.tight_layout() to compactify the plots
"""
# Plot Fourier series coefficients
def plot_fsc(f, N_max, x, dx, name, filename):
    # 1. get all Fourier series coefficients
    a_0, a, b = fsc_all(N_max, f, x, dx)
    # 2. set a_0 and b_0 = 0 as first elements of a, b
    # a.insert(0,a_0) 
    a = [a_0] + a
    b_0 = 0
    b = [b_0] + b
    # b.insert(0,0)
    # 3. plot Fourier series coefficients a, b
    fig = plt.figure() 
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.bar(range(N_max+1),a)
    ax1.set_title(f"Coefficents for a and b for {name}")
    ax2.bar(range(N_max+1),b)
    plt.savefig(f"{filename}")

# sample periodic functions (signals)
def f_square(x): return np.where(x >= 0, 1, 0)
def f_triangle(x): return np.where(x >=0, -x, x)
def f_sawtooth(x): return x
def f_rectifier(x): return np.where(x >= 0, x, 0)

# main function
if __name__ == "__main__":
    # specify dx: the distance between x-values over [-pi,+pi]
    dx = 1/100
    # number of points in [-pi, +pi] using width dx
    m = int(2 * np.pi / dx)
    # list of m x-axis values in [-pi, +pi]
    x = np.linspace(-np.pi, np.pi, m)

    # specify the three values of N (# terms in series)
    N1, N2, N3 = 2, 20, 200
    # call plot_fsr with four different signals defined above
    plot_fsr(f_square, N1, N2, N3, x, dx, 'square','HW4-FSR-Square.pdf')
    plot_fsr(f_triangle, N1, N2, N3, x, dx, 'triangle', 'HW4-FSR-Triangle.pdf')
    plot_fsr(f_sawtooth, N1, N2, N3, x, dx, 'sawtooth', 'HW4-FSR-Sawtooth.pdf')
    plot_fsr(f_rectifier, N1, N2, N3, x, dx, 'rectifier', 'HW4-FSR-Rectifier.pdf')

    # specify the maximum value of N needed below
    N_max = 200
    # call plot_fse with four different signals defined above
    plot_fse(f_square, N_max, x, dx, 'square', 'HW4-FSE-Square.pdf')
    plot_fse(f_triangle, N_max, x, dx, 'triangle', 'HW4-FSE-Triangle.pdf')
    plot_fse(f_sawtooth, N_max, x, dx, 'sawtooth', 'HW4-FSE-Sawtooth.pdf')
    plot_fse(f_rectifier, N_max, x, dx, 'rectifier', 'HW4-FSE-Rectifier.pdf')

    # call plot_fsc with four different signals defined above
    plot_fsc(f_square, N_max, x, dx, 'square', 'HW4-FSC-Square.pdf')
    plot_fsc(f_triangle, N_max, x, dx, 'triangle', 'HW4-FSC-Triangle.pdf')
    plot_fsc(f_sawtooth, N_max, x, dx, 'sawtooth', 'HW4-FSC-Sawtooth.pdf')
    plot_fsc(f_rectifier, N_max, x, dx, 'rectifier', 'HW4-FSC-Rectifier.pdf')
