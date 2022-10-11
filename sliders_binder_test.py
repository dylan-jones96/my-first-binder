from matplotlib.widgets import Slider, Button
from tables import *

import numpy as np
import matplotlib.pyplot as plt


def make_sliders():

    # Make a horizontal slider to control deltaU1.
    ax_deltaU1 = fig.add_axes([0.25, 0.12, 0.65, 0.03])
    set_deltaU1_slider = Slider(
        ax=ax_deltaU1,
        label=r'$\Delta U1$',
        valmin=0.0,
        valmax=0.5,
        valinit=init_deltaU1,
        valstep=0.1,
    )

    # Make a horizontal slider to control deltaU2.
    ax_deltaU2 = fig.add_axes([0.25, 0.16, 0.65, 0.03])
    set_deltaU2_slider = Slider(
        ax=ax_deltaU2,
        label=r'$\Delta U2$',
        valmin=0.0,
        valmax=0.5,
        valinit=init_deltaU2,
        valstep=0.1,
    )

    return set_deltaU1_slider, set_deltaU2_slider


# Load bands data from files.
def get_bands(potential_period, potential_height, t, tp, tsoc, deltaU1, deltaU2):

    params_path_potential = 'VL' + '{0:.0f}'.format(potential_period) + '_VH' + '{0:.3f}'.format(potential_height)
    params_path_hoppings = '_t' + '{0:.2f}'.format(t) + '_tp' + '{0:.2f}'.format(tp) + \
                           '_tsoc' + '{0:.2f}'.format(tsoc)
    params_path_onsite = '_deltaU1' + '{0:.2f}'.format(deltaU1) + '_deltaU2' + '{0:.2f}'.format(deltaU2)
    total_filename = params_path_potential + params_path_hoppings + params_path_onsite

    bands = h5file_data.get_node('/VL2_data', 'bands_'+total_filename)

    return bands


# The function to be called anytime a slider's value changes.
def update(val):

    ax.clear()
    bands_to_plot = get_bands(potential_period=2, potential_height=0.0, t=-1.0,
                              tp=-0.05, tsoc=0.0, deltaU1=deltaU1_slider.val,
                              deltaU2=deltaU2_slider.val)
    for band_ind in range(0, len(bands_to_plot[0]), 1):
        ax.plot(k_points, bands_to_plot[:, band_ind], color=colors[0], lw=0.8)

    # line.set_ydata(f(t, amp_slider.val, freq_slider.val))
    fig.canvas.draw_idle()


# Reset button.
def reset(event):
    deltaU1_slider.reset()
    deltaU2_slider.reset()

# Load in hdf5 data file.
h5file_data = open_file('all_data.h5', 'r')

# Get default plotting colour.
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# Initial parameter values.
init_potential_period = 2.0
init_potential_height = 0.0
init_t = -1.0
init_tp = -0.05
init_tsoc = 0.0
init_deltaU1 = 0.0
init_deltaU2 = 0.0

# Get x_axis data.
k_path = h5file_data.get_node('/VL2_data', 'k_path')
k_points = h5file_data.get_node('/VL2_data', 'k_points')
point_indices = h5file_data.get_node('/VL2_data', 'point_indices')
tick_labels = [r'$\Gamma$', 'X', 'M', 'Y', r'$\Gamma$', 'M']
# Get bands.
init_bands = get_bands(init_potential_period, init_potential_height, init_t, init_tp, init_tsoc,
                       init_deltaU1, init_deltaU2)


# Plot initial figure.
fig, ax = plt.subplots(figsize=[10, 8])
for band_ind_init in range(0, len(init_bands[0]), 1):
    ax.plot(k_points, init_bands[:, band_ind_init], color=colors[0], lw=0.8)

# Adjust the main plot to make room for the sliders.
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make the sliders.
deltaU1_slider, deltaU2_slider = make_sliders()

# Register the update function with each slider.
deltaU1_slider.on_changed(update)
deltaU2_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
reset_ax = fig.add_axes([0.05, 0.1, 0.1, 0.04])
button = Button(reset_ax, 'Reset', hovercolor='0.975')
button.on_clicked(reset)

plt.show()
