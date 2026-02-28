from jinja2 import Template

def refresh(target,context):
    return Template(target).render(context)