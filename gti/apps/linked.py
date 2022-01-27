import pandas as pd
import panel as pn

from . import descr


# Linked table as an empty Tabulator widget
df = pd.DataFrame(
    dict(
        code_idx=[0, 0, 0, 1, 2],
        item=['Rain', 'Sleet', 'Snow', 'T-shirt', 'Joy'],
        datetime=pd.date_range('2021-12-1 12:00', '2022-1-21 12:00', periods=5),
    )
)

table = pn.widgets.Tabulator(
    df.head(0),
    disabled=True, # disable editing => clicking anywhere selects the row
    header_filters=dict( # exclude datetime field so widget displays properly
        code_idx=dict(type='input', func='='),
        item=dict(type='input'),
    ),
    # hidden_columns=['code_idx'],
    pagination='remote',
    page_size=3,
    selectable=1,
    show_index=False,
    height=200,
)


# Single-row table to display the currently selected descr
descr_display = pn.widgets.Tabulator(
    descr.df.head(0),
    disabled=True,
    header_filters=False,
    # hidden_columns=['dummy'],
    show_index=False,
    selectable=False,
    height=80,
)


# Widget to select a descr through its index
# (will be linked to the descr.table.selection)
descr_idx = pn.widgets.IntInput(
    name='descr index',
    start=descr.df.index.min(),
    end=descr.df.index.max(),
    width=100,
)

def descr_callback(*events):
    for event in events:
        if event.name == 'value':
            df_l = df[df.code_idx == event.new]
            table.value = df_l
            table.selection = []

            df_d = descr.df.loc[event.new : event.new]
            descr_display.value = df_d

descr_idx_watcher = descr_idx.param.watch(
    fn=descr_callback,
    parameter_names=['value'],
    onlychanged=False,
)


ui = pn.Column(
    name='Linked UI',
    objects=[
        descr_display,
        # descr_idx,
        table,
    ],
)
