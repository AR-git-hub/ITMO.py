from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),  # или PackageLoader?
    autoescape=select_autoescape()
)

def render_template(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context)
