import pandas as pd
import panel as pn


# Description table as an empty Tabulator widget
descr = [
    'Under the Weather',
    'Top Drawer',
    'Happy as a Clam',
]

code = [f'{i+1:02d}' for i in range(len(descr))]

dummy = ['dummy'] * len(descr)

df = pd.DataFrame(
    dict(
        code=code,
        descr=descr,
        dummy=dummy,
    )
)

table = pn.widgets.Tabulator(
    df.head(0),
    disabled=True, # disable editing => clicking anywhere selects the row
    header_filters=True,
    hidden_columns=['dummy'],
    pagination='remote',
    page_size=3,
    selectable=1,
    show_index=False,
    height=200,
)

# Button to load the table data
btn_load = pn.widgets.Button(
    name='(Re)load',
    button_type='primary',
)

def load(event):
    table.value = df

btn_load.on_click(load)


# Button to add a new row to the table
btn_add = pn.widgets.Button(
    name='Add new row',
    button_type='danger',
    # disabled=True,
)

def add(event):
    """ Add a new row to the table.

    The code and descr are set by the current header filter values,
    and the row is only added if there is no already matching row.
    """
    global df
    if (
        (len(table.filters) == 2) # both header filters must be active
        and
        (table.current_view.size == 0) # and showing no matching rows
       ):
        df = df.append({f['field']: f['value']
                        for f in table.filters},
                       ignore_index=True)

        load(None) # reload the (updated) table
        table.param.trigger('filters') # refresh the filtered view

btn_add.on_click(add)


ui = pn.Column(
    name='Description UI',
    objects=[
        btn_load,
        table,
        btn_add,
    ]
)
