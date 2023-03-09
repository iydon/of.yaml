__all__ = ['AddOn']


import typing as t

if t.TYPE_CHECKING:
    import typing_extensions as te

    from . import Figure


Wrapper = t.Callable[..., 'Figure']


class AddOn:
    '''matplotlib

    CodeGen:
        ```python
        __import__('warnings').filterwarnings('ignore')

        import matplotlib.pyplot as plt

        judges = [
            lambda name: name.startswith('_') or name.endswith('_'),
            lambda name: any(map(str.isupper, name)),
        ]
        fig, ax = plt.subplots(1, 1)
        for name in dir(ax):
            if any(judge(name) for judge in judges):
                continue
            attr = getattr(ax, name)
            if not callable(attr):
                continue
            print(f"    {name}: Wrapper = lambda self, *args, **kwargs: self._wrapper('{name}', *args, **kwargs)")
        ```
    '''

    def __init__(self, figure: 'Figure') -> None:
        self._figure = figure
        self._ret = None

    @classmethod
    def new(cls, *args: t.Any, **kwargs: t.Any) -> 'te.Self':
        return cls(*args, **kwargs)

    @property
    def ret(self) -> t.Any:
        return self._ret

    def _wrapper(self, name: str, /, *args: t.Any, **kwargs: t.Any) -> 'Figure':
        self._ret = getattr(self._figure._ax, name)(*args, **kwargs)
        return self._figure

    acorr: Wrapper = lambda self, *args, **kwargs: self._wrapper('acorr', *args, **kwargs)
    add_artist: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_artist', *args, **kwargs)
    add_callback: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_callback', *args, **kwargs)
    add_child_axes: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_child_axes', *args, **kwargs)
    add_collection: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_collection', *args, **kwargs)
    add_container: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_container', *args, **kwargs)
    add_image: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_image', *args, **kwargs)
    add_line: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_line', *args, **kwargs)
    add_patch: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_patch', *args, **kwargs)
    add_table: Wrapper = lambda self, *args, **kwargs: self._wrapper('add_table', *args, **kwargs)
    angle_spectrum: Wrapper = lambda self, *args, **kwargs: self._wrapper('angle_spectrum', *args, **kwargs)
    annotate: Wrapper = lambda self, *args, **kwargs: self._wrapper('annotate', *args, **kwargs)
    apply_aspect: Wrapper = lambda self, *args, **kwargs: self._wrapper('apply_aspect', *args, **kwargs)
    arrow: Wrapper = lambda self, *args, **kwargs: self._wrapper('arrow', *args, **kwargs)
    autoscale: Wrapper = lambda self, *args, **kwargs: self._wrapper('autoscale', *args, **kwargs)
    autoscale_view: Wrapper = lambda self, *args, **kwargs: self._wrapper('autoscale_view', *args, **kwargs)
    axhline: Wrapper = lambda self, *args, **kwargs: self._wrapper('axhline', *args, **kwargs)
    axhspan: Wrapper = lambda self, *args, **kwargs: self._wrapper('axhspan', *args, **kwargs)
    axis: Wrapper = lambda self, *args, **kwargs: self._wrapper('axis', *args, **kwargs)
    axline: Wrapper = lambda self, *args, **kwargs: self._wrapper('axline', *args, **kwargs)
    axvline: Wrapper = lambda self, *args, **kwargs: self._wrapper('axvline', *args, **kwargs)
    axvspan: Wrapper = lambda self, *args, **kwargs: self._wrapper('axvspan', *args, **kwargs)
    bar: Wrapper = lambda self, *args, **kwargs: self._wrapper('bar', *args, **kwargs)
    bar_label: Wrapper = lambda self, *args, **kwargs: self._wrapper('bar_label', *args, **kwargs)
    barbs: Wrapper = lambda self, *args, **kwargs: self._wrapper('barbs', *args, **kwargs)
    barh: Wrapper = lambda self, *args, **kwargs: self._wrapper('barh', *args, **kwargs)
    boxplot: Wrapper = lambda self, *args, **kwargs: self._wrapper('boxplot', *args, **kwargs)
    broken_barh: Wrapper = lambda self, *args, **kwargs: self._wrapper('broken_barh', *args, **kwargs)
    bxp: Wrapper = lambda self, *args, **kwargs: self._wrapper('bxp', *args, **kwargs)
    can_pan: Wrapper = lambda self, *args, **kwargs: self._wrapper('can_pan', *args, **kwargs)
    can_zoom: Wrapper = lambda self, *args, **kwargs: self._wrapper('can_zoom', *args, **kwargs)
    change_geometry: Wrapper = lambda self, *args, **kwargs: self._wrapper('change_geometry', *args, **kwargs)
    cla: Wrapper = lambda self, *args, **kwargs: self._wrapper('cla', *args, **kwargs)
    clabel: Wrapper = lambda self, *args, **kwargs: self._wrapper('clabel', *args, **kwargs)
    clear: Wrapper = lambda self, *args, **kwargs: self._wrapper('clear', *args, **kwargs)
    cohere: Wrapper = lambda self, *args, **kwargs: self._wrapper('cohere', *args, **kwargs)
    contains: Wrapper = lambda self, *args, **kwargs: self._wrapper('contains', *args, **kwargs)
    contains_point: Wrapper = lambda self, *args, **kwargs: self._wrapper('contains_point', *args, **kwargs)
    contour: Wrapper = lambda self, *args, **kwargs: self._wrapper('contour', *args, **kwargs)
    contourf: Wrapper = lambda self, *args, **kwargs: self._wrapper('contourf', *args, **kwargs)
    convert_xunits: Wrapper = lambda self, *args, **kwargs: self._wrapper('convert_xunits', *args, **kwargs)
    convert_yunits: Wrapper = lambda self, *args, **kwargs: self._wrapper('convert_yunits', *args, **kwargs)
    csd: Wrapper = lambda self, *args, **kwargs: self._wrapper('csd', *args, **kwargs)
    drag_pan: Wrapper = lambda self, *args, **kwargs: self._wrapper('drag_pan', *args, **kwargs)
    draw: Wrapper = lambda self, *args, **kwargs: self._wrapper('draw', *args, **kwargs)
    draw_artist: Wrapper = lambda self, *args, **kwargs: self._wrapper('draw_artist', *args, **kwargs)
    end_pan: Wrapper = lambda self, *args, **kwargs: self._wrapper('end_pan', *args, **kwargs)
    errorbar: Wrapper = lambda self, *args, **kwargs: self._wrapper('errorbar', *args, **kwargs)
    eventplot: Wrapper = lambda self, *args, **kwargs: self._wrapper('eventplot', *args, **kwargs)
    fill: Wrapper = lambda self, *args, **kwargs: self._wrapper('fill', *args, **kwargs)
    fill_between: Wrapper = lambda self, *args, **kwargs: self._wrapper('fill_between', *args, **kwargs)
    fill_betweenx: Wrapper = lambda self, *args, **kwargs: self._wrapper('fill_betweenx', *args, **kwargs)
    findobj: Wrapper = lambda self, *args, **kwargs: self._wrapper('findobj', *args, **kwargs)
    format_coord: Wrapper = lambda self, *args, **kwargs: self._wrapper('format_coord', *args, **kwargs)
    format_cursor_data: Wrapper = lambda self, *args, **kwargs: self._wrapper('format_cursor_data', *args, **kwargs)
    format_xdata: Wrapper = lambda self, *args, **kwargs: self._wrapper('format_xdata', *args, **kwargs)
    format_ydata: Wrapper = lambda self, *args, **kwargs: self._wrapper('format_ydata', *args, **kwargs)
    get_adjustable: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_adjustable', *args, **kwargs)
    get_agg_filter: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_agg_filter', *args, **kwargs)
    get_alpha: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_alpha', *args, **kwargs)
    get_anchor: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_anchor', *args, **kwargs)
    get_animated: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_animated', *args, **kwargs)
    get_aspect: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_aspect', *args, **kwargs)
    get_autoscale_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_autoscale_on', *args, **kwargs)
    get_autoscalex_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_autoscalex_on', *args, **kwargs)
    get_autoscaley_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_autoscaley_on', *args, **kwargs)
    get_axes_locator: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_axes_locator', *args, **kwargs)
    get_axisbelow: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_axisbelow', *args, **kwargs)
    get_box_aspect: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_box_aspect', *args, **kwargs)
    get_children: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_children', *args, **kwargs)
    get_clip_box: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_clip_box', *args, **kwargs)
    get_clip_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_clip_on', *args, **kwargs)
    get_clip_path: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_clip_path', *args, **kwargs)
    get_cursor_data: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_cursor_data', *args, **kwargs)
    get_data_ratio: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_data_ratio', *args, **kwargs)
    get_default_bbox_extra_artists: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_default_bbox_extra_artists', *args, **kwargs)
    get_facecolor: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_facecolor', *args, **kwargs)
    get_fc: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_fc', *args, **kwargs)
    get_figure: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_figure', *args, **kwargs)
    get_frame_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_frame_on', *args, **kwargs)
    get_geometry: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_geometry', *args, **kwargs)
    get_gid: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_gid', *args, **kwargs)
    get_gridspec: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_gridspec', *args, **kwargs)
    get_images: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_images', *args, **kwargs)
    get_in_layout: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_in_layout', *args, **kwargs)
    get_label: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_label', *args, **kwargs)
    get_legend: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_legend', *args, **kwargs)
    get_legend_handles_labels: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_legend_handles_labels', *args, **kwargs)
    get_lines: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_lines', *args, **kwargs)
    get_navigate: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_navigate', *args, **kwargs)
    get_navigate_mode: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_navigate_mode', *args, **kwargs)
    get_path_effects: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_path_effects', *args, **kwargs)
    get_picker: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_picker', *args, **kwargs)
    get_position: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_position', *args, **kwargs)
    get_rasterization_zorder: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_rasterization_zorder', *args, **kwargs)
    get_rasterized: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_rasterized', *args, **kwargs)
    get_renderer_cache: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_renderer_cache', *args, **kwargs)
    get_shared_x_axes: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_shared_x_axes', *args, **kwargs)
    get_shared_y_axes: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_shared_y_axes', *args, **kwargs)
    get_sketch_params: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_sketch_params', *args, **kwargs)
    get_snap: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_snap', *args, **kwargs)
    get_subplotspec: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_subplotspec', *args, **kwargs)
    get_tightbbox: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_tightbbox', *args, **kwargs)
    get_title: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_title', *args, **kwargs)
    get_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_transform', *args, **kwargs)
    get_transformed_clip_path_and_affine: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_transformed_clip_path_and_affine', *args, **kwargs)
    get_url: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_url', *args, **kwargs)
    get_visible: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_visible', *args, **kwargs)
    get_window_extent: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_window_extent', *args, **kwargs)
    get_xaxis: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xaxis', *args, **kwargs)
    get_xaxis_text1_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xaxis_text1_transform', *args, **kwargs)
    get_xaxis_text2_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xaxis_text2_transform', *args, **kwargs)
    get_xaxis_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xaxis_transform', *args, **kwargs)
    get_xbound: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xbound', *args, **kwargs)
    get_xgridlines: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xgridlines', *args, **kwargs)
    get_xlabel: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xlabel', *args, **kwargs)
    get_xlim: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xlim', *args, **kwargs)
    get_xmajorticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xmajorticklabels', *args, **kwargs)
    get_xminorticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xminorticklabels', *args, **kwargs)
    get_xscale: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xscale', *args, **kwargs)
    get_xticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xticklabels', *args, **kwargs)
    get_xticklines: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xticklines', *args, **kwargs)
    get_xticks: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_xticks', *args, **kwargs)
    get_yaxis: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yaxis', *args, **kwargs)
    get_yaxis_text1_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yaxis_text1_transform', *args, **kwargs)
    get_yaxis_text2_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yaxis_text2_transform', *args, **kwargs)
    get_yaxis_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yaxis_transform', *args, **kwargs)
    get_ybound: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_ybound', *args, **kwargs)
    get_ygridlines: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_ygridlines', *args, **kwargs)
    get_ylabel: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_ylabel', *args, **kwargs)
    get_ylim: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_ylim', *args, **kwargs)
    get_ymajorticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_ymajorticklabels', *args, **kwargs)
    get_yminorticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yminorticklabels', *args, **kwargs)
    get_yscale: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yscale', *args, **kwargs)
    get_yticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yticklabels', *args, **kwargs)
    get_yticklines: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yticklines', *args, **kwargs)
    get_yticks: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_yticks', *args, **kwargs)
    get_zorder: Wrapper = lambda self, *args, **kwargs: self._wrapper('get_zorder', *args, **kwargs)
    grid: Wrapper = lambda self, *args, **kwargs: self._wrapper('grid', *args, **kwargs)
    has_data: Wrapper = lambda self, *args, **kwargs: self._wrapper('has_data', *args, **kwargs)
    have_units: Wrapper = lambda self, *args, **kwargs: self._wrapper('have_units', *args, **kwargs)
    hexbin: Wrapper = lambda self, *args, **kwargs: self._wrapper('hexbin', *args, **kwargs)
    hist: Wrapper = lambda self, *args, **kwargs: self._wrapper('hist', *args, **kwargs)
    hist2d: Wrapper = lambda self, *args, **kwargs: self._wrapper('hist2d', *args, **kwargs)
    hlines: Wrapper = lambda self, *args, **kwargs: self._wrapper('hlines', *args, **kwargs)
    imshow: Wrapper = lambda self, *args, **kwargs: self._wrapper('imshow', *args, **kwargs)
    in_axes: Wrapper = lambda self, *args, **kwargs: self._wrapper('in_axes', *args, **kwargs)
    indicate_inset: Wrapper = lambda self, *args, **kwargs: self._wrapper('indicate_inset', *args, **kwargs)
    indicate_inset_zoom: Wrapper = lambda self, *args, **kwargs: self._wrapper('indicate_inset_zoom', *args, **kwargs)
    inset_axes: Wrapper = lambda self, *args, **kwargs: self._wrapper('inset_axes', *args, **kwargs)
    invert_xaxis: Wrapper = lambda self, *args, **kwargs: self._wrapper('invert_xaxis', *args, **kwargs)
    invert_yaxis: Wrapper = lambda self, *args, **kwargs: self._wrapper('invert_yaxis', *args, **kwargs)
    is_first_col: Wrapper = lambda self, *args, **kwargs: self._wrapper('is_first_col', *args, **kwargs)
    is_first_row: Wrapper = lambda self, *args, **kwargs: self._wrapper('is_first_row', *args, **kwargs)
    is_last_col: Wrapper = lambda self, *args, **kwargs: self._wrapper('is_last_col', *args, **kwargs)
    is_last_row: Wrapper = lambda self, *args, **kwargs: self._wrapper('is_last_row', *args, **kwargs)
    is_transform_set: Wrapper = lambda self, *args, **kwargs: self._wrapper('is_transform_set', *args, **kwargs)
    label_outer: Wrapper = lambda self, *args, **kwargs: self._wrapper('label_outer', *args, **kwargs)
    legend: Wrapper = lambda self, *args, **kwargs: self._wrapper('legend', *args, **kwargs)
    locator_params: Wrapper = lambda self, *args, **kwargs: self._wrapper('locator_params', *args, **kwargs)
    loglog: Wrapper = lambda self, *args, **kwargs: self._wrapper('loglog', *args, **kwargs)
    magnitude_spectrum: Wrapper = lambda self, *args, **kwargs: self._wrapper('magnitude_spectrum', *args, **kwargs)
    margins: Wrapper = lambda self, *args, **kwargs: self._wrapper('margins', *args, **kwargs)
    matshow: Wrapper = lambda self, *args, **kwargs: self._wrapper('matshow', *args, **kwargs)
    minorticks_off: Wrapper = lambda self, *args, **kwargs: self._wrapper('minorticks_off', *args, **kwargs)
    minorticks_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('minorticks_on', *args, **kwargs)
    pchanged: Wrapper = lambda self, *args, **kwargs: self._wrapper('pchanged', *args, **kwargs)
    pcolor: Wrapper = lambda self, *args, **kwargs: self._wrapper('pcolor', *args, **kwargs)
    pcolorfast: Wrapper = lambda self, *args, **kwargs: self._wrapper('pcolorfast', *args, **kwargs)
    pcolormesh: Wrapper = lambda self, *args, **kwargs: self._wrapper('pcolormesh', *args, **kwargs)
    phase_spectrum: Wrapper = lambda self, *args, **kwargs: self._wrapper('phase_spectrum', *args, **kwargs)
    pick: Wrapper = lambda self, *args, **kwargs: self._wrapper('pick', *args, **kwargs)
    pickable: Wrapper = lambda self, *args, **kwargs: self._wrapper('pickable', *args, **kwargs)
    pie: Wrapper = lambda self, *args, **kwargs: self._wrapper('pie', *args, **kwargs)
    plot: Wrapper = lambda self, *args, **kwargs: self._wrapper('plot', *args, **kwargs)
    plot_date: Wrapper = lambda self, *args, **kwargs: self._wrapper('plot_date', *args, **kwargs)
    properties: Wrapper = lambda self, *args, **kwargs: self._wrapper('properties', *args, **kwargs)
    psd: Wrapper = lambda self, *args, **kwargs: self._wrapper('psd', *args, **kwargs)
    quiver: Wrapper = lambda self, *args, **kwargs: self._wrapper('quiver', *args, **kwargs)
    quiverkey: Wrapper = lambda self, *args, **kwargs: self._wrapper('quiverkey', *args, **kwargs)
    redraw_in_frame: Wrapper = lambda self, *args, **kwargs: self._wrapper('redraw_in_frame', *args, **kwargs)
    relim: Wrapper = lambda self, *args, **kwargs: self._wrapper('relim', *args, **kwargs)
    remove: Wrapper = lambda self, *args, **kwargs: self._wrapper('remove', *args, **kwargs)
    remove_callback: Wrapper = lambda self, *args, **kwargs: self._wrapper('remove_callback', *args, **kwargs)
    reset_position: Wrapper = lambda self, *args, **kwargs: self._wrapper('reset_position', *args, **kwargs)
    scatter: Wrapper = lambda self, *args, **kwargs: self._wrapper('scatter', *args, **kwargs)
    secondary_xaxis: Wrapper = lambda self, *args, **kwargs: self._wrapper('secondary_xaxis', *args, **kwargs)
    secondary_yaxis: Wrapper = lambda self, *args, **kwargs: self._wrapper('secondary_yaxis', *args, **kwargs)
    semilogx: Wrapper = lambda self, *args, **kwargs: self._wrapper('semilogx', *args, **kwargs)
    semilogy: Wrapper = lambda self, *args, **kwargs: self._wrapper('semilogy', *args, **kwargs)
    set: Wrapper = lambda self, *args, **kwargs: self._wrapper('set', *args, **kwargs)
    set_adjustable: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_adjustable', *args, **kwargs)
    set_agg_filter: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_agg_filter', *args, **kwargs)
    set_alpha: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_alpha', *args, **kwargs)
    set_anchor: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_anchor', *args, **kwargs)
    set_animated: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_animated', *args, **kwargs)
    set_aspect: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_aspect', *args, **kwargs)
    set_autoscale_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_autoscale_on', *args, **kwargs)
    set_autoscalex_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_autoscalex_on', *args, **kwargs)
    set_autoscaley_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_autoscaley_on', *args, **kwargs)
    set_axes_locator: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_axes_locator', *args, **kwargs)
    set_axis_off: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_axis_off', *args, **kwargs)
    set_axis_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_axis_on', *args, **kwargs)
    set_axisbelow: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_axisbelow', *args, **kwargs)
    set_box_aspect: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_box_aspect', *args, **kwargs)
    set_clip_box: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_clip_box', *args, **kwargs)
    set_clip_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_clip_on', *args, **kwargs)
    set_clip_path: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_clip_path', *args, **kwargs)
    set_facecolor: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_facecolor', *args, **kwargs)
    set_fc: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_fc', *args, **kwargs)
    set_figure: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_figure', *args, **kwargs)
    set_frame_on: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_frame_on', *args, **kwargs)
    set_gid: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_gid', *args, **kwargs)
    set_in_layout: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_in_layout', *args, **kwargs)
    set_label: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_label', *args, **kwargs)
    set_navigate: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_navigate', *args, **kwargs)
    set_navigate_mode: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_navigate_mode', *args, **kwargs)
    set_path_effects: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_path_effects', *args, **kwargs)
    set_picker: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_picker', *args, **kwargs)
    set_position: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_position', *args, **kwargs)
    set_prop_cycle: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_prop_cycle', *args, **kwargs)
    set_rasterization_zorder: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_rasterization_zorder', *args, **kwargs)
    set_rasterized: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_rasterized', *args, **kwargs)
    set_sketch_params: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_sketch_params', *args, **kwargs)
    set_snap: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_snap', *args, **kwargs)
    set_subplotspec: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_subplotspec', *args, **kwargs)
    set_title: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_title', *args, **kwargs)
    set_transform: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_transform', *args, **kwargs)
    set_url: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_url', *args, **kwargs)
    set_visible: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_visible', *args, **kwargs)
    set_xbound: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_xbound', *args, **kwargs)
    set_xlabel: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_xlabel', *args, **kwargs)
    set_xlim: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_xlim', *args, **kwargs)
    set_xmargin: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_xmargin', *args, **kwargs)
    set_xscale: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_xscale', *args, **kwargs)
    set_xticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_xticklabels', *args, **kwargs)
    set_xticks: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_xticks', *args, **kwargs)
    set_ybound: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_ybound', *args, **kwargs)
    set_ylabel: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_ylabel', *args, **kwargs)
    set_ylim: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_ylim', *args, **kwargs)
    set_ymargin: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_ymargin', *args, **kwargs)
    set_yscale: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_yscale', *args, **kwargs)
    set_yticklabels: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_yticklabels', *args, **kwargs)
    set_yticks: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_yticks', *args, **kwargs)
    set_zorder: Wrapper = lambda self, *args, **kwargs: self._wrapper('set_zorder', *args, **kwargs)
    sharex: Wrapper = lambda self, *args, **kwargs: self._wrapper('sharex', *args, **kwargs)
    sharey: Wrapper = lambda self, *args, **kwargs: self._wrapper('sharey', *args, **kwargs)
    specgram: Wrapper = lambda self, *args, **kwargs: self._wrapper('specgram', *args, **kwargs)
    spy: Wrapper = lambda self, *args, **kwargs: self._wrapper('spy', *args, **kwargs)
    stackplot: Wrapper = lambda self, *args, **kwargs: self._wrapper('stackplot', *args, **kwargs)
    stairs: Wrapper = lambda self, *args, **kwargs: self._wrapper('stairs', *args, **kwargs)
    stale_callback: Wrapper = lambda self, *args, **kwargs: self._wrapper('stale_callback', *args, **kwargs)
    start_pan: Wrapper = lambda self, *args, **kwargs: self._wrapper('start_pan', *args, **kwargs)
    stem: Wrapper = lambda self, *args, **kwargs: self._wrapper('stem', *args, **kwargs)
    step: Wrapper = lambda self, *args, **kwargs: self._wrapper('step', *args, **kwargs)
    streamplot: Wrapper = lambda self, *args, **kwargs: self._wrapper('streamplot', *args, **kwargs)
    table: Wrapper = lambda self, *args, **kwargs: self._wrapper('table', *args, **kwargs)
    text: Wrapper = lambda self, *args, **kwargs: self._wrapper('text', *args, **kwargs)
    tick_params: Wrapper = lambda self, *args, **kwargs: self._wrapper('tick_params', *args, **kwargs)
    ticklabel_format: Wrapper = lambda self, *args, **kwargs: self._wrapper('ticklabel_format', *args, **kwargs)
    tricontour: Wrapper = lambda self, *args, **kwargs: self._wrapper('tricontour', *args, **kwargs)
    tricontourf: Wrapper = lambda self, *args, **kwargs: self._wrapper('tricontourf', *args, **kwargs)
    tripcolor: Wrapper = lambda self, *args, **kwargs: self._wrapper('tripcolor', *args, **kwargs)
    triplot: Wrapper = lambda self, *args, **kwargs: self._wrapper('triplot', *args, **kwargs)
    twinx: Wrapper = lambda self, *args, **kwargs: self._wrapper('twinx', *args, **kwargs)
    twiny: Wrapper = lambda self, *args, **kwargs: self._wrapper('twiny', *args, **kwargs)
    update: Wrapper = lambda self, *args, **kwargs: self._wrapper('update', *args, **kwargs)
    update_datalim: Wrapper = lambda self, *args, **kwargs: self._wrapper('update_datalim', *args, **kwargs)
    update_from: Wrapper = lambda self, *args, **kwargs: self._wrapper('update_from', *args, **kwargs)
    update_params: Wrapper = lambda self, *args, **kwargs: self._wrapper('update_params', *args, **kwargs)
    violin: Wrapper = lambda self, *args, **kwargs: self._wrapper('violin', *args, **kwargs)
    violinplot: Wrapper = lambda self, *args, **kwargs: self._wrapper('violinplot', *args, **kwargs)
    vlines: Wrapper = lambda self, *args, **kwargs: self._wrapper('vlines', *args, **kwargs)
    xaxis_date: Wrapper = lambda self, *args, **kwargs: self._wrapper('xaxis_date', *args, **kwargs)
    xaxis_inverted: Wrapper = lambda self, *args, **kwargs: self._wrapper('xaxis_inverted', *args, **kwargs)
    xcorr: Wrapper = lambda self, *args, **kwargs: self._wrapper('xcorr', *args, **kwargs)
    yaxis_date: Wrapper = lambda self, *args, **kwargs: self._wrapper('yaxis_date', *args, **kwargs)
    yaxis_inverted: Wrapper = lambda self, *args, **kwargs: self._wrapper('yaxis_inverted', *args, **kwargs)
