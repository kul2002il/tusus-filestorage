import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pathlib import Path


def load_time_and_signals_from_csv(filename):
    dataframe = pd.read_csv(
        filename,
        sep=';',
        decimal=',',
        skipinitialspace=True,
    )
    dataframe = dataframe.dropna(axis=1, how='all')
    time = dataframe[dataframe.columns[0]].to_numpy()
    signals = {column: dataframe[column].to_numpy()
               for column in dataframe.columns[1:]}
    return time, signals


def get_time_by_trigger(time, signal, trigger):
    time = np.asarray(time, dtype=float)
    signal = np.asarray(signal, dtype=float)

    if time.shape != signal.shape:
        raise ValueError('time и signal должны иметь одинаковую длину')
    if time.size < 2:
        return np.array([])

    shifted = signal - trigger
    crossing_indices = np.where(np.sign(shifted[:-1]) * np.sign(shifted[1:]) < 0)[0]

    if crossing_indices.size == 0:
        return np.array([])

    t0 = time[crossing_indices]
    t1 = time[crossing_indices + 1]
    s0 = shifted[crossing_indices]
    s1 = shifted[crossing_indices + 1]
    return t0 - s0 * (t1 - t0) / (s1 - s0)


def make_axes(signal_count, height_per_plot=2.5, width=10):
    figure, axes = plt.subplots(
        nrows=signal_count,
        ncols=1,
        sharex=True,
        figsize=(width, height_per_plot * signal_count),
        gridspec_kw={'hspace': 0},
    )
    if signal_count == 1:
        axes = [axes]
    for axis in axes:
        axis.margins(x=0)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=10))
    return figure, axes


def style_axes_with_arrows(axis):
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_linewidth(1.2)
    axis.spines['left'].set_linewidth(1.2)
    axis.plot(1, 0, ">k", transform=axis.get_yaxis_transform(),
              clip_on=False, markersize=8)
    axis.plot(0, 1, "^k", transform=axis.get_xaxis_transform(),
              clip_on=False, markersize=8)


def plot_signals(axes, time, signals):
    for axis, (name, values) in zip(axes, signals.items()):
        axis.plot(time, values, linewidth=1, color="black", label=name)
        axis.set_ylabel(name)
        axis.grid(True, alpha=0.3)


def add_vertical_line(axes, position):
    for axis in axes:
        axis.axvline(x=position, linestyle='--', linewidth=1, color="black")


def add_horizontal_line(axis, position):
    axis.axhline(y=position, linestyle='--', linewidth=1, color="black")


def draw_dimension_line(axis, point_start, point_end, label,
                        offset=0.0, fontsize=10, color='black'):
    x_start, y_start = point_start
    x_end, y_end = point_end

    axis.annotate(
        '',
        xy=point_end,
        xytext=point_start,
        arrowprops=dict(
            arrowstyle='<->',
            color=color,
            linewidth=1.5,
            shrinkA=0,
            shrinkB=0,
        ),
    )

    start_display = axis.transData.transform((x_start, y_start))
    end_display = axis.transData.transform((x_end, y_end))
    dx_display = end_display[0] - start_display[0]
    dy_display = end_display[1] - start_display[1]

    angle_degrees = np.degrees(np.arctan2(dy_display, dx_display))
    if angle_degrees > 90 or angle_degrees < -90:
        angle_degrees += 180

    x_mid = (x_start + x_end) / 2
    y_mid = (y_start + y_end) / 2

    length_display = np.hypot(dx_display, dy_display)
    if length_display == 0:
        return

    perp_display_x = -dy_display / length_display
    perp_display_y = dx_display / length_display

    mid_display = axis.transData.transform((x_mid, y_mid))
    text_display = mid_display + np.array([perp_display_x, perp_display_y]) * offset
    text_x, text_y = axis.transData.inverted().transform(text_display)

    axis.text(
        text_x, text_y, label,
        rotation=angle_degrees,
        rotation_mode='anchor',
        ha='center', va='bottom',
        fontsize=fontsize,
        color=color,
    )


def create_associated_svg_filename(filename):
    return str(Path(filename).with_suffix('.svg'))


def main():
    filename = "/home/ilia/MY_FILES/ТУСУР/СЭС/КР/Попытка рисовать графики/первый_график.csv"
    time, signals = load_time_and_signals_from_csv(filename)

    switch_times = get_time_by_trigger(time, signals["V(/U_int_in)"], 0)
    bottom = min(signals["V(/U_int_out)"])
    top = max(signals["V(/U_int_out)"])

    figure, axes = make_axes(len(signals))

    plot_signals(axes, time, signals)

    for switch_time in switch_times:
        add_vertical_line(axes, switch_time)
    add_horizontal_line(axes[1], bottom)
    add_horizontal_line(axes[1], top)
    draw_dimension_line(axes[1], (0.014, bottom), (0.014, top), 'U_p-p')

    figure.tight_layout()
    figure.savefig(create_associated_svg_filename(filename))


if __name__ == '__main__':
    main()