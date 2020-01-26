from IPython.display import display, HTML

class Semantic_CSS:
    colors = ['red', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue', 'violet', 'purple', 'pink', 'brown', 'black']

    def setup(self):
        html = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.css" integrity="sha256-QVBN0oT74UhpCtEo4Ko+k3sNo+ykJFBBtGduw13V9vw=" crossorigin="anonymous" />'
        display(HTML(html))
        return self

    def message(self, message, color='teal'):
        html = '<div class="ui {0} message">{1}</div>'.format(color,message)
        display(HTML(html))

    def title_and_subtitle(self, title, sub_title):
        html = '<h2 class="ui header">{0}<div class="sub header">{1}</div></h2>'.format(title, sub_title)
        return self.show(html)

    def show(self,html):
        display(HTML(html))
        return self