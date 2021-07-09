"""Script for plotting radar charts.

This script allows for plotting a radar chart. This script requires that `numpy` and `matplotlib` be installed within
the Python environment you are running this script in.
"""

from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def radar_chart(
    labels: Union[List[str], np.ndarray, pd.Series],
    values: Union[List[float], np.ndarray, pd.Series],
    groups: Optional[Union[List[float], np.ndarray, pd.Series]] = None,
    marker_size: int = 4,
    line_width: int = 1,
    label_size: int = 10,
    label_color: str = "black",
    label_padding: int = 25,
    ytick_labels: bool = False,
    fill_alpha: float = 0.25,
    figure_size: Tuple[int, int] = (6, 4),
    title: str = None,
    title_size: int = 16,
    draw_grid: bool = True,
    grid_line_color: str = "#888888",
    grid_line_width: float = 0.3,
    legend_position: Tuple[float, float] = (1.0, 1.0),
    save_path: Optional[str] = None,
) -> None:
    """Plot a radar/spider chart.

    Parameters
    ----------
    labels : Union[List[str], np.ndarray, pd.Series]
        A list, numpy array or pandas Series of strings that serve as labels on the radar chart.
    values : Union[List[float], np.ndarray, pd.Series]
        A list, numpy array or pandas Series of floats that serve as values on the radar chart.
    groups : Optional[Union[List[float], np.ndarray, pd.Series]]
        A list, numpy array or pandas Series of strings to create multiple radar chars on the same axis, by default None
    marker_size : int, optional
        Size of the marker, by default 4
    line_width : int, optional
        Line width of the polygon, by default 1
    label_size : int, optional
        Size of the label font, by default 10
    label_color : str, optional
        Color of the labels, by default "black"
    label_padding : int, optional
        Distance between the labels and the radar plot, by default 25
    ytick_labels : bool, optional
        Whether to display y tick labels, by default False
    fill_alpha : float, optional
        Opacity of the fill of the polygon, by default 0.20
    figure_size : Tuple[float, float], optional
        Size of the figure, by default (6, 4)
    title : str, optional
        Title of the plot, by default None
    title_size : int, optional
        Font size of the title, by default 16
    draw_grid : bool, optional
        Whether or not to draw a grid, by default True
    grid_line_color : str, optional
        Color of the grid, by default "#888888"
    grid_line_width : float, optional
        Line width of the grid, by default 0.3
    legend_position : Tuple[float, float], optional
        Postion of the legend, by default (1.0, 1.0)
    save_path : Optional[str], optional
        Path to save your radar chart to, by default None

    Raises
    ------
    Exception
        Raised when the amount of value and group samples are not the same.

    Examples
    --------

    First simple example.

    >>> import matplotlib.pyplot as plt
    >>> from radar import radar_chart
    >>> labels = ["A", "B", "C", "D", "E", "F"]
    >>> values = [0, 2, 1, 6, 4, 5]
    >>> radar_chart(labels=labels, values=values)
    >>> plt.show()

    Second example demonstrating multiple polygons in one chart.

    >>> skills = ["Skills", "Defence", "Mental", "Physical", "Passing", "Shooting", "Goalkeeper"]
    >>> scores = [[95, 20, 48, 96, 81, 64, 20],
                  [77, 93, 93, 53, 67, 87, 11],
                  [30, 27, 34, 13, 43, 15, 90]]
    >>> players = [["Lionel Messi"],
                   ["Virgil van Dijk"],
                   ["Jan Oblak"]]
    >>> radar_chart(labels=labels, values=values, groups=players)
    >>> plt.show()
    """
    # Make list a list of list
    if len(labels) == len(values):
        values = [values]

    # Convert lists to numpy arrays
    labels = np.array(labels)
    values = np.array(values)

    # Set initial figure parameters
    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot(111, projection="polar")

    theta = np.arange(len(labels) + 1) / float(len(labels)) * 2 * np.pi

    # Draw the marksers/line and polygon
    for index, value in enumerate(values):
        value = np.append(value, value[0])

        # Check for multi polygons
        if groups:
            if np.array(groups).shape[0] != values.shape[0]:
                raise Exception(
                    f"To visualize multiple polygons the value and group arrays should have the same number of "
                    f"samples. The value array has {values.shape[0]} samples and group array has "
                    f"{np.array(groups).shape[0]} samples. "
                )
            group = groups[index][0]
        else:
            group = f"Group {index + 1}"
        ax.plot(
            theta,
            value,
            marker="o",
            markersize=marker_size,
            linewidth=line_width,
            label=str(group),
            zorder=1,
        )
        ax.fill(theta, value, alpha=fill_alpha)

        if len(values) != 1:
            ax.legend(loc="best", bbox_to_anchor=legend_position, frameon=False)

    # Set ticks and labels
    plt.xticks(theta[:-1], labels, color=label_color, size=label_size)
    if ytick_labels is False:
        ax.set_yticklabels([])

    # Set tick padding
    ax.tick_params(pad=label_padding)

    # Set title of the chart
    if title:
        fig.suptitle(title, fontsize=title_size)

    # Grid parameters
    if draw_grid:
        ax.grid(True, color=grid_line_color, linewidth=grid_line_width)
    else:
        ax.grid(False)

    plt.tight_layout()

    # Save image
    if save_path:
        plt.savefig(save_path)
