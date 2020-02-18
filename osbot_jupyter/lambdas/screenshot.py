from gw_bot.lambdas.png_to_slack import load_dependencies


def run(event, context):
    load_dependencies('requests,syncer,pyppeteer')

    from osbot_jupyter.api.Live_Notebook import Live_Notebook

    short_id = event.get('short_id')
    path     = event.get('path')
    width    = event.get('width')
    height   = event.get('height')
    delay    = event.get('delay')
    notebook = Live_Notebook()

    notebook.set_build_from_short_id(short_id)

    return notebook.screenshot(path=path,width=width,height=height, delay=delay)
