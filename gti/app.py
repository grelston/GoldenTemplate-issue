import panel as pn

from .apps import descr, linked


golden = pn.template.GoldenTemplate(title='Linked Tabulators')

def link_tabs(*events):
    for event in events:
        if event.name == 'selection':
            idx = event.obj.selected_dataframe.index
            val = None if idx.empty else idx[0].item()
            linked.descr_idx.value = val

descr.table.param.watch(
    fn=link_tabs,
    parameter_names=['selection'],
    onlychanged=False,
)

golden.sidebar.append(linked.descr_display)

golden.main.append(descr.ui)
golden.main.append(linked.ui)

golden.servable(title='LT app')
