"""
xblock helpers.
"""
import os
from html.parser import HTMLParser

from django.template import Context, Engine

html_parser = HTMLParser()  # pylint: disable=invalid-name


def render_template(template_name, **context):
    """
    Render static resource using provided context.

    Returns: django.utils.safestring.SafeText
    """
    template_dirs = [os.path.join(os.path.dirname(__file__), "static/html")]
    libraries = {"clickaware_tags": "clickaware.templatetags"}
    engine = Engine(dirs=template_dirs, debug=True, libraries=libraries)
    html = engine.get_template(template_name)

    return html_parser.unescape(html.render(Context(context)))
