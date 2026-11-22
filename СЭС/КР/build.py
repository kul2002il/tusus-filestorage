# build.py
from itertools import chain
import scripts.graph as graph

def build_time_flow_circuits_without_diodes(
) -> None:
    # Ввод

    input_filename_csv = "Симуляции схем/Анализ имеющихся решений/Схема с интегратором/Результаты симуляции/схема без диодов.csv"
    out_filename = "images/built/временная диаграмма интегратора без диодов.svg"

    time, signals = graph.load_time_and_signals_from_csv(input_filename_csv, {
        'V(/U_int_in)',
        'V(/U_int_out)',
    })

    # Анализ

    rising_fronts = graph.get_time_by_trigger(time, signals["V(/U_int_in)"], 0, 'rising')
    falling_fronts = graph.get_time_by_trigger(time, signals["V(/U_int_in)"], 0, 'falling')
    top = max(signals["V(/U_int_out)"])
    bottom = min(signals["V(/U_int_out)"])

    # Отрисовка

    figure, axes = graph.make_axes(2)
    graph.plot_signal(axes[0], time, signals["V(/U_int_in)"], "V(U_int_in)")
    graph.plot_signal(axes[1], time, signals["V(/U_int_out)"], "V(U_int_out)")

    for switch_time in chain(rising_fronts, falling_fronts):
        graph.add_vertical_line(axes, switch_time)

    graph.add_horizontal_line(axes[1], top, "U_out_max")
    graph.add_horizontal_line(axes[1], bottom, "U_out_min")
    graph.draw_dimension_line(axes[1], (rising_fronts[1], bottom), (rising_fronts[1], top), '2U_out_max')
    graph.draw_dimension_line(axes[1], (rising_fronts[0], bottom * 1.4), (falling_fronts[0], bottom * 1.4), 't_спад')
    graph.draw_dimension_line(axes[1], (falling_fronts[0], bottom * 1.4), (rising_fronts[1], bottom * 1.4), 't_раст')
    graph.draw_dimension_line(axes[1], (rising_fronts[0], bottom * 1.8), (rising_fronts[1], bottom * 1.8), 'T')

    graph.adjust_figure_padding(figure)
    figure.savefig(out_filename)
    graph.plt.close(figure)

    print(f"Сохранено: {out_filename}")

def build_time_flow_circuits_with_diodes(
) -> None:
    # Ввод

    input_filename_csv = "Симуляции схем/Анализ имеющихся решений/Схема с интегратором/Результаты симуляции/схема с диодами.csv"
    out_filename = "images/built/временная диаграмма интегратора с диодами.svg"

    time, signals = graph.load_time_and_signals_from_csv(input_filename_csv, {
        'V(/U_int_in)',
        'V(/U_int_out)',
        'I(Rint1)',
        'I(Rint2)',
    })

    # Анализ

    rising_fronts = graph.get_time_by_trigger(time, signals["V(/U_int_in)"], 0, 'rising')
    falling_fronts = graph.get_time_by_trigger(time, signals["V(/U_int_in)"], 0, 'falling')
    top = max(signals["V(/U_int_out)"])
    bottom = min(signals["V(/U_int_out)"])

    # Отрисовка

    figure, axes = graph.make_axes(3)
    graph.plot_signal(axes[0], time, signals["V(/U_int_in)"], "V(U_int_in)")
    graph.plot_signal(axes[1], time, signals["I(Rint1)"])
    graph.plot_signal(axes[1], time, signals["I(Rint2)"], "I(Rint1, Rint2)", line_style=":", marker="o")
    graph.plot_signal(axes[2], time, signals["V(/U_int_out)"], "V(U_int_out)")

    for switch_time in chain(rising_fronts, falling_fronts):
        graph.add_vertical_line(axes, switch_time)

    graph.add_horizontal_line(axes[2], top, "U_out_max")
    graph.add_horizontal_line(axes[2], bottom, "U_out_min")
    graph.draw_dimension_line(axes[2], (rising_fronts[1], bottom), (rising_fronts[1], top), '2U_out_max')
    graph.draw_dimension_line(axes[2], (rising_fronts[0], bottom * 1.4), (falling_fronts[0], bottom * 1.4), 't_спад')
    graph.draw_dimension_line(axes[2], (falling_fronts[0], bottom * 1.4), (rising_fronts[1], bottom * 1.4), 't_раст')
    graph.draw_dimension_line(axes[2], (rising_fronts[0], bottom * 1.8), (rising_fronts[1], bottom * 1.8), 'T')

    graph.adjust_figure_padding(figure)
    figure.savefig(out_filename)
    graph.plt.close(figure)

    print(f"Сохранено: {out_filename}")

def main():
    build_time_flow_circuits_without_diodes()
    build_time_flow_circuits_with_diodes()


if __name__ == '__main__':
    main()