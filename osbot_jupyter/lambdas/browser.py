


def run(event, context):
    from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
    browser = Browser_Lamdba_Helper().setup()
    return 'ok'
    # from osbot_aws.apis.Lambda import load_dependencies
    # load_dependencies(['syncer','pyppeteer'])
    # from osbot_browser.browser.API_Browser import API_Browser
    # browser = API_Browser()
    # return browser.sync__url()
