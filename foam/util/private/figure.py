__all__ = ['Figure']


import pathlib as p
import typing as t

from ..function import deprecated_classmethod
from ...base.lib import matplotlib
from ...base.type import Path

if t.TYPE_CHECKING:
    import matplotlib.axes as _axes
    import matplotlib.figure as _figure

    from typing_extensions import Self


class Figure:
    '''Matplotlib simple wrapper

    Example:
        >>> Figure.setRcParams(
        ...     ('axes.unicode_minus', False),
        ...     ('font.sans-serif', ['FandolHei']),
        ... )
        >>> Figure.new(figsize=(8, 6)) \\
        ...     .plot([1, 2, 3], [3, 2, 1], label='a') \\
        ...     .plot([1, 2, 3], [2, 1, 3], label='b') \\
        ...     .set(xlabel='x label', ylabel='y label', title='title') \\
        ...     .grid() \\
        ...     .legend() \\
        ...     .save('demo.png')

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
            print(f"    def {name}(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('{name}', *args, **kwargs)")
        ```
    '''

    DEFAULT = {
        'legend': {
            'bbox_to_anchor': (1.01, 1), 'loc': 'upper left',
            'borderaxespad': 0, 'ncol': 1,
        },
        'save': {'bbox_inches': 'tight', 'transparent': False},
    }

    _ax: '_axes.SubplotBase'
    _fig: '_figure.Figure'

    def __init__(self, **kwargs: t.Any) -> None:
        self._fig, self._ax = matplotlib.pyplot.subplots(1, 1, **kwargs)
        self._ret = None

    @classmethod
    def new(cls, **kwargs: t.Any) -> 'Self':
        return cls(**kwargs)

    @classmethod
    def setRcParams(cls, *items: t.Tuple[str, t.Any]) -> 'Self':
        # Type annotation of return value should actually be type
        for key, value in items:
            matplotlib.pyplot.rcParams[key] = value
        return cls

    @property
    def ax(self) -> '_axes.SubplotBase':
        return self._ax

    @property
    def fig(self) -> '_figure.Figure':
        return self._fig

    @property
    def ret(self) -> t.Any:
        return self._ret

    def save(self, path: Path, **kwargs: t.Any) -> 'Self':
        kwargs = {**self.DEFAULT['save'], **kwargs}
        self._fig.savefig(p.Path(path).as_posix(), **kwargs)
        return self

    def acorr(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('acorr', *args, **kwargs)
    def add_artist(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_artist', *args, **kwargs)
    def add_callback(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_callback', *args, **kwargs)
    def add_child_axes(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_child_axes', *args, **kwargs)
    def add_collection(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_collection', *args, **kwargs)
    def add_container(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_container', *args, **kwargs)
    def add_image(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_image', *args, **kwargs)
    def add_line(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_line', *args, **kwargs)
    def add_patch(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_patch', *args, **kwargs)
    def add_table(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('add_table', *args, **kwargs)
    def angle_spectrum(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('angle_spectrum', *args, **kwargs)
    def annotate(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('annotate', *args, **kwargs)
    def apply_aspect(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('apply_aspect', *args, **kwargs)
    def arrow(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('arrow', *args, **kwargs)
    def autoscale(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('autoscale', *args, **kwargs)
    def autoscale_view(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('autoscale_view', *args, **kwargs)
    def axhline(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('axhline', *args, **kwargs)
    def axhspan(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('axhspan', *args, **kwargs)
    def axis(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('axis', *args, **kwargs)
    def axline(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('axline', *args, **kwargs)
    def axvline(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('axvline', *args, **kwargs)
    def axvspan(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('axvspan', *args, **kwargs)
    def bar(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('bar', *args, **kwargs)
    def bar_label(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('bar_label', *args, **kwargs)
    def barbs(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('barbs', *args, **kwargs)
    def barh(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('barh', *args, **kwargs)
    def boxplot(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('boxplot', *args, **kwargs)
    def broken_barh(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('broken_barh', *args, **kwargs)
    def bxp(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('bxp', *args, **kwargs)
    def can_pan(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('can_pan', *args, **kwargs)
    def can_zoom(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('can_zoom', *args, **kwargs)
    def change_geometry(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('change_geometry', *args, **kwargs)
    def cla(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('cla', *args, **kwargs)
    def clabel(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('clabel', *args, **kwargs)
    def clear(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('clear', *args, **kwargs)
    def cohere(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('cohere', *args, **kwargs)
    def contains(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('contains', *args, **kwargs)
    def contains_point(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('contains_point', *args, **kwargs)
    def contour(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('contour', *args, **kwargs)
    def contourf(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('contourf', *args, **kwargs)
    def convert_xunits(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('convert_xunits', *args, **kwargs)
    def convert_yunits(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('convert_yunits', *args, **kwargs)
    def csd(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('csd', *args, **kwargs)
    def drag_pan(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('drag_pan', *args, **kwargs)
    def draw(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('draw', *args, **kwargs)
    def draw_artist(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('draw_artist', *args, **kwargs)
    def end_pan(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('end_pan', *args, **kwargs)
    def errorbar(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('errorbar', *args, **kwargs)
    def eventplot(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('eventplot', *args, **kwargs)
    def fill(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('fill', *args, **kwargs)
    def fill_between(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('fill_between', *args, **kwargs)
    def fill_betweenx(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('fill_betweenx', *args, **kwargs)
    def findobj(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('findobj', *args, **kwargs)
    def format_coord(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('format_coord', *args, **kwargs)
    def format_cursor_data(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('format_cursor_data', *args, **kwargs)
    def format_xdata(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('format_xdata', *args, **kwargs)
    def format_ydata(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('format_ydata', *args, **kwargs)
    def get_adjustable(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_adjustable', *args, **kwargs)
    def get_agg_filter(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_agg_filter', *args, **kwargs)
    def get_alpha(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_alpha', *args, **kwargs)
    def get_anchor(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_anchor', *args, **kwargs)
    def get_animated(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_animated', *args, **kwargs)
    def get_aspect(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_aspect', *args, **kwargs)
    def get_autoscale_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_autoscale_on', *args, **kwargs)
    def get_autoscalex_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_autoscalex_on', *args, **kwargs)
    def get_autoscaley_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_autoscaley_on', *args, **kwargs)
    def get_axes_locator(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_axes_locator', *args, **kwargs)
    def get_axisbelow(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_axisbelow', *args, **kwargs)
    def get_box_aspect(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_box_aspect', *args, **kwargs)
    def get_children(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_children', *args, **kwargs)
    def get_clip_box(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_clip_box', *args, **kwargs)
    def get_clip_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_clip_on', *args, **kwargs)
    def get_clip_path(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_clip_path', *args, **kwargs)
    def get_cursor_data(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_cursor_data', *args, **kwargs)
    def get_data_ratio(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_data_ratio', *args, **kwargs)
    def get_default_bbox_extra_artists(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_default_bbox_extra_artists', *args, **kwargs)
    def get_facecolor(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_facecolor', *args, **kwargs)
    def get_fc(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_fc', *args, **kwargs)
    def get_figure(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_figure', *args, **kwargs)
    def get_frame_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_frame_on', *args, **kwargs)
    def get_geometry(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_geometry', *args, **kwargs)
    def get_gid(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_gid', *args, **kwargs)
    def get_gridspec(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_gridspec', *args, **kwargs)
    def get_images(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_images', *args, **kwargs)
    def get_in_layout(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_in_layout', *args, **kwargs)
    def get_label(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_label', *args, **kwargs)
    def get_legend(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_legend', *args, **kwargs)
    def get_legend_handles_labels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_legend_handles_labels', *args, **kwargs)
    def get_lines(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_lines', *args, **kwargs)
    def get_navigate(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_navigate', *args, **kwargs)
    def get_navigate_mode(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_navigate_mode', *args, **kwargs)
    def get_path_effects(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_path_effects', *args, **kwargs)
    def get_picker(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_picker', *args, **kwargs)
    def get_position(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_position', *args, **kwargs)
    def get_rasterization_zorder(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_rasterization_zorder', *args, **kwargs)
    def get_rasterized(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_rasterized', *args, **kwargs)
    def get_renderer_cache(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_renderer_cache', *args, **kwargs)
    def get_shared_x_axes(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_shared_x_axes', *args, **kwargs)
    def get_shared_y_axes(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_shared_y_axes', *args, **kwargs)
    def get_sketch_params(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_sketch_params', *args, **kwargs)
    def get_snap(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_snap', *args, **kwargs)
    def get_subplotspec(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_subplotspec', *args, **kwargs)
    def get_tightbbox(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_tightbbox', *args, **kwargs)
    def get_title(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_title', *args, **kwargs)
    def get_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_transform', *args, **kwargs)
    def get_transformed_clip_path_and_affine(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_transformed_clip_path_and_affine', *args, **kwargs)
    def get_url(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_url', *args, **kwargs)
    def get_visible(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_visible', *args, **kwargs)
    def get_window_extent(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_window_extent', *args, **kwargs)
    def get_xaxis(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xaxis', *args, **kwargs)
    def get_xaxis_text1_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xaxis_text1_transform', *args, **kwargs)
    def get_xaxis_text2_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xaxis_text2_transform', *args, **kwargs)
    def get_xaxis_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xaxis_transform', *args, **kwargs)
    def get_xbound(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xbound', *args, **kwargs)
    def get_xgridlines(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xgridlines', *args, **kwargs)
    def get_xlabel(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xlabel', *args, **kwargs)
    def get_xlim(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xlim', *args, **kwargs)
    def get_xmajorticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xmajorticklabels', *args, **kwargs)
    def get_xminorticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xminorticklabels', *args, **kwargs)
    def get_xscale(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xscale', *args, **kwargs)
    def get_xticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xticklabels', *args, **kwargs)
    def get_xticklines(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xticklines', *args, **kwargs)
    def get_xticks(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_xticks', *args, **kwargs)
    def get_yaxis(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yaxis', *args, **kwargs)
    def get_yaxis_text1_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yaxis_text1_transform', *args, **kwargs)
    def get_yaxis_text2_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yaxis_text2_transform', *args, **kwargs)
    def get_yaxis_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yaxis_transform', *args, **kwargs)
    def get_ybound(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_ybound', *args, **kwargs)
    def get_ygridlines(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_ygridlines', *args, **kwargs)
    def get_ylabel(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_ylabel', *args, **kwargs)
    def get_ylim(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_ylim', *args, **kwargs)
    def get_ymajorticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_ymajorticklabels', *args, **kwargs)
    def get_yminorticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yminorticklabels', *args, **kwargs)
    def get_yscale(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yscale', *args, **kwargs)
    def get_yticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yticklabels', *args, **kwargs)
    def get_yticklines(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yticklines', *args, **kwargs)
    def get_yticks(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_yticks', *args, **kwargs)
    def get_zorder(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('get_zorder', *args, **kwargs)
    def grid(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('grid', *args, **kwargs)
    def has_data(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('has_data', *args, **kwargs)
    def have_units(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('have_units', *args, **kwargs)
    def hexbin(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('hexbin', *args, **kwargs)
    def hist(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('hist', *args, **kwargs)
    def hist2d(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('hist2d', *args, **kwargs)
    def hlines(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('hlines', *args, **kwargs)
    def imshow(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('imshow', *args, **kwargs)
    def in_axes(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('in_axes', *args, **kwargs)
    def indicate_inset(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('indicate_inset', *args, **kwargs)
    def indicate_inset_zoom(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('indicate_inset_zoom', *args, **kwargs)
    def inset_axes(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('inset_axes', *args, **kwargs)
    def invert_xaxis(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('invert_xaxis', *args, **kwargs)
    def invert_yaxis(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('invert_yaxis', *args, **kwargs)
    def is_first_col(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('is_first_col', *args, **kwargs)
    def is_first_row(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('is_first_row', *args, **kwargs)
    def is_last_col(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('is_last_col', *args, **kwargs)
    def is_last_row(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('is_last_row', *args, **kwargs)
    def is_transform_set(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('is_transform_set', *args, **kwargs)
    def label_outer(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('label_outer', *args, **kwargs)
    def legend(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('legend', *args, **kwargs)
    def locator_params(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('locator_params', *args, **kwargs)
    def loglog(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('loglog', *args, **kwargs)
    def magnitude_spectrum(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('magnitude_spectrum', *args, **kwargs)
    def margins(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('margins', *args, **kwargs)
    def matshow(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('matshow', *args, **kwargs)
    def minorticks_off(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('minorticks_off', *args, **kwargs)
    def minorticks_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('minorticks_on', *args, **kwargs)
    def pchanged(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('pchanged', *args, **kwargs)
    def pcolor(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('pcolor', *args, **kwargs)
    def pcolorfast(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('pcolorfast', *args, **kwargs)
    def pcolormesh(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('pcolormesh', *args, **kwargs)
    def phase_spectrum(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('phase_spectrum', *args, **kwargs)
    def pick(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('pick', *args, **kwargs)
    def pickable(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('pickable', *args, **kwargs)
    def pie(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('pie', *args, **kwargs)
    def plot(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('plot', *args, **kwargs)
    def plot_date(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('plot_date', *args, **kwargs)
    def properties(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('properties', *args, **kwargs)
    def psd(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('psd', *args, **kwargs)
    def quiver(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('quiver', *args, **kwargs)
    def quiverkey(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('quiverkey', *args, **kwargs)
    def redraw_in_frame(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('redraw_in_frame', *args, **kwargs)
    def relim(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('relim', *args, **kwargs)
    def remove(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('remove', *args, **kwargs)
    def remove_callback(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('remove_callback', *args, **kwargs)
    def reset_position(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('reset_position', *args, **kwargs)
    def scatter(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('scatter', *args, **kwargs)
    def secondary_xaxis(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('secondary_xaxis', *args, **kwargs)
    def secondary_yaxis(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('secondary_yaxis', *args, **kwargs)
    def semilogx(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('semilogx', *args, **kwargs)
    def semilogy(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('semilogy', *args, **kwargs)
    def set(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set', *args, **kwargs)
    def set_adjustable(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_adjustable', *args, **kwargs)
    def set_agg_filter(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_agg_filter', *args, **kwargs)
    def set_alpha(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_alpha', *args, **kwargs)
    def set_anchor(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_anchor', *args, **kwargs)
    def set_animated(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_animated', *args, **kwargs)
    def set_aspect(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_aspect', *args, **kwargs)
    def set_autoscale_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_autoscale_on', *args, **kwargs)
    def set_autoscalex_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_autoscalex_on', *args, **kwargs)
    def set_autoscaley_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_autoscaley_on', *args, **kwargs)
    def set_axes_locator(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_axes_locator', *args, **kwargs)
    def set_axis_off(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_axis_off', *args, **kwargs)
    def set_axis_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_axis_on', *args, **kwargs)
    def set_axisbelow(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_axisbelow', *args, **kwargs)
    def set_box_aspect(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_box_aspect', *args, **kwargs)
    def set_clip_box(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_clip_box', *args, **kwargs)
    def set_clip_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_clip_on', *args, **kwargs)
    def set_clip_path(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_clip_path', *args, **kwargs)
    def set_facecolor(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_facecolor', *args, **kwargs)
    def set_fc(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_fc', *args, **kwargs)
    def set_figure(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_figure', *args, **kwargs)
    def set_frame_on(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_frame_on', *args, **kwargs)
    def set_gid(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_gid', *args, **kwargs)
    def set_in_layout(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_in_layout', *args, **kwargs)
    def set_label(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_label', *args, **kwargs)
    def set_navigate(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_navigate', *args, **kwargs)
    def set_navigate_mode(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_navigate_mode', *args, **kwargs)
    def set_path_effects(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_path_effects', *args, **kwargs)
    def set_picker(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_picker', *args, **kwargs)
    def set_position(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_position', *args, **kwargs)
    def set_prop_cycle(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_prop_cycle', *args, **kwargs)
    def set_rasterization_zorder(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_rasterization_zorder', *args, **kwargs)
    def set_rasterized(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_rasterized', *args, **kwargs)
    def set_sketch_params(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_sketch_params', *args, **kwargs)
    def set_snap(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_snap', *args, **kwargs)
    def set_subplotspec(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_subplotspec', *args, **kwargs)
    def set_title(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_title', *args, **kwargs)
    def set_transform(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_transform', *args, **kwargs)
    def set_url(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_url', *args, **kwargs)
    def set_visible(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_visible', *args, **kwargs)
    def set_xbound(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_xbound', *args, **kwargs)
    def set_xlabel(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_xlabel', *args, **kwargs)
    def set_xlim(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_xlim', *args, **kwargs)
    def set_xmargin(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_xmargin', *args, **kwargs)
    def set_xscale(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_xscale', *args, **kwargs)
    def set_xticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_xticklabels', *args, **kwargs)
    def set_xticks(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_xticks', *args, **kwargs)
    def set_ybound(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_ybound', *args, **kwargs)
    def set_ylabel(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_ylabel', *args, **kwargs)
    def set_ylim(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_ylim', *args, **kwargs)
    def set_ymargin(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_ymargin', *args, **kwargs)
    def set_yscale(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_yscale', *args, **kwargs)
    def set_yticklabels(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_yticklabels', *args, **kwargs)
    def set_yticks(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_yticks', *args, **kwargs)
    def set_zorder(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('set_zorder', *args, **kwargs)
    def sharex(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('sharex', *args, **kwargs)
    def sharey(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('sharey', *args, **kwargs)
    def specgram(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('specgram', *args, **kwargs)
    def spy(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('spy', *args, **kwargs)
    def stackplot(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('stackplot', *args, **kwargs)
    def stairs(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('stairs', *args, **kwargs)
    def stale_callback(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('stale_callback', *args, **kwargs)
    def start_pan(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('start_pan', *args, **kwargs)
    def stem(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('stem', *args, **kwargs)
    def step(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('step', *args, **kwargs)
    def streamplot(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('streamplot', *args, **kwargs)
    def table(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('table', *args, **kwargs)
    def text(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('text', *args, **kwargs)
    def tick_params(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('tick_params', *args, **kwargs)
    def ticklabel_format(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('ticklabel_format', *args, **kwargs)
    def tricontour(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('tricontour', *args, **kwargs)
    def tricontourf(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('tricontourf', *args, **kwargs)
    def tripcolor(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('tripcolor', *args, **kwargs)
    def triplot(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('triplot', *args, **kwargs)
    def twinx(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('twinx', *args, **kwargs)
    def twiny(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('twiny', *args, **kwargs)
    def update(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('update', *args, **kwargs)
    def update_datalim(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('update_datalim', *args, **kwargs)
    def update_from(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('update_from', *args, **kwargs)
    def update_params(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('update_params', *args, **kwargs)
    def violin(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('violin', *args, **kwargs)
    def violinplot(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('violinplot', *args, **kwargs)
    def vlines(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('vlines', *args, **kwargs)
    def xaxis_date(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('xaxis_date', *args, **kwargs)
    def xaxis_inverted(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('xaxis_inverted', *args, **kwargs)
    def xcorr(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('xcorr', *args, **kwargs)
    def yaxis_date(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('yaxis_date', *args, **kwargs)
    def yaxis_inverted(self, *args: t.Any, **kwargs: t.Any) -> 'Self': return self._bind_ax('yaxis_inverted', *args, **kwargs)

    def _bind_ax(self, name: str, /, *args: t.Any, **kwargs: t.Any) -> 'Self':
        if name in self.DEFAULT:
            kwargs = {**self.DEFAULT[name], **kwargs}
        self._ret = getattr(self._ax, name)(*args, **kwargs)
        return self

    set_rc_params = deprecated_classmethod(setRcParams)
