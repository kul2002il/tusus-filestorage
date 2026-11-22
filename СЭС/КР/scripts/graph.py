# scripts/graph.py
from collections.abc import Callable
from pathlib import Path
from typing import Literal, TypeAlias

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

# Удобные псевдонимы — читаемость сигнатур
Signals: TypeAlias = dict[str, np.ndarray]
AnnotationCallback: TypeAlias = Callable[[list[Axes], np.ndarray, Signals], None]

fontsize = 14

def load_time_and_signals_from_csv(
    filename: str | Path,
    required_keys
) -> tuple[np.ndarray, Signals]:
    dataframe: pd.DataFrame = pd.read_csv(
        filename,
        sep=';',
        decimal=',',
        skipinitialspace=True,
    )
    dataframe = dataframe.dropna(axis=1, how='all')
    time: np.ndarray = dataframe[dataframe.columns[0]].to_numpy()
    signals: Signals = {
        column: dataframe[column].to_numpy()
        for column in dataframe.columns[1:]
    }

    missing_keys = required_keys - signals.keys()

    if missing_keys:
        message = (
            f"В файле <{filename}>\n"
            f"отсутствуют сигналы: {missing_keys}.\n"
            f"Доступные сигналы: {list(signals.keys())}.\n"
        )
        raise ValueError(message)

    return time, signals

EdgeType = Literal['any', 'rising', 'falling']
def get_time_by_trigger(
    time: np.ndarray,
    signal: np.ndarray,
    trigger: float,
    edge: EdgeType = 'any',
) -> np.ndarray:
    """
    Возвращает времена пересечения сигналом уровня trigger.

    edge : 'any'    — любое пересечение (по умолчанию)
           'rising' — только нарастающий фронт
           'falling'— только спадающий фронт
    """
    if edge not in ('any', 'rising', 'falling'):
        raise ValueError("edge должен быть 'any', 'rising' или 'falling'")

    time = np.asarray(time, dtype=float)
    signal = np.asarray(signal, dtype=float)

    if time.shape != signal.shape:
        raise ValueError('time и signal должны иметь одинаковую длину')
    if time.size < 2:
        return np.array([])

    shifted = signal - trigger

    if edge == 'rising':
        crossing_indices = np.where((shifted[:-1] < 0) & (shifted[1:] > 0))[0]
    elif edge == 'falling':
        crossing_indices = np.where((shifted[:-1] > 0) & (shifted[1:] < 0))[0]
    else:
        crossing_indices = np.where(
            np.sign(shifted[:-1]) * np.sign(shifted[1:]) < 0
        )[0]

    if crossing_indices.size == 0:
        return np.array([])

    t0 = time[crossing_indices]
    t1 = time[crossing_indices + 1]
    s0 = shifted[crossing_indices]
    s1 = shifted[crossing_indices + 1]
    return t0 - s0 * (t1 - t0) / (s1 - s0)


def make_axes(
    signal_count: int,
    height_per_plot: float = 2.5,
    width: float = 10,
) -> tuple[Figure, list[Axes]]:
    figure, axes = plt.subplots(
        nrows=signal_count,
        ncols=1,
        sharex=True,
        figsize=(width, height_per_plot * signal_count),
        gridspec_kw={'hspace': 0},
    )
    axes_list: list[Axes] = list(axes) if signal_count > 1 else [axes]
    for axis in axes_list:
        axis.margins(x=0, y=0.2)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=10))
    return figure, axes_list

def adjust_figure_padding(figure: Figure) -> None:
    figure.subplots_adjust(left=0.10, right=0.98, top=0.98, bottom=0.06, hspace=0)

LineStyle = Literal['-', '--', '-.', ':']
MarkerStyle = Literal['o', 's', '^', 'v', 'D', 'x', '+', '*', '.', ',']

def plot_signal(
    axis: Axes,
    time: np.ndarray,
    signal: np.ndarray,
    name: str = '',
    line_style: LineStyle = '-',
    marker: MarkerStyle | None = None,
) -> None:
    axis.plot(
        time, signal,
        linewidth=1,
        color="black",
        label=name,
        linestyle=line_style,
        marker=marker,
        markersize=5,
        markevery=len(signal)//10,
    )
    axis.set_ylabel(name, fontsize=fontsize)
    axis.grid(True, alpha=0.3)


def add_vertical_line(axes: list[Axes], x: float) -> None:
    for axis in axes:
        axis.axvline(x=x, linestyle='--', linewidth=1, color="black")


def add_horizontal_line(axis: Axes, y: float, label: str = '') -> None:
    axis.axhline(y=y, linestyle='--', linewidth=1, color="black")

    if label:
        axis.annotate(
            label,
            xy=(0, y),
            xycoords=('axes fraction', 'data'),
            xytext=(4, 2),
            textcoords='offset points',
            ha='left',
            va='bottom',
            fontsize=fontsize,
            color='black',
        )


def draw_dimension_line(
    axis: Axes,
    point_start: tuple[float, float],
    point_end: tuple[float, float],
    label: str,
) -> None:
    x_start, y_start = point_start
    x_end, y_end = point_end

    axis.plot([x_start, x_end], [y_start, y_end], linestyle='none', marker='', alpha=0)

    axis.annotate(
        '',
        xy=point_end,
        xytext=point_start,
        arrowprops=dict(
            arrowstyle='<->',
            color='black',
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
    text_display = mid_display + np.array([perp_display_x, perp_display_y])
    text_x, text_y = axis.transData.inverted().transform(text_display)

    axis.text(
        text_x, text_y, label,
        rotation=angle_degrees,
        rotation_mode='anchor',
        ha='center', va='bottom',
        fontsize=fontsize,
        color='black',
    )
