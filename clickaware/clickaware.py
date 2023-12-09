"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from django.utils.translation import ugettext as _
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, Scope, String
from xblock.completable import XBlockCompletionMode, CompletableXBlockMixin

from .utils import render_template


@XBlock.needs("i18n")
class ClickAwareXBlock(XBlock, CompletableXBlockMixin):
    icon_class = "other"
    # Setting this attribute to standard means that this XBlock
    # takes part in completion tracking.
    completion_mode = XBlockCompletionMode.COMPLETABLE

    def has_custom_completion(self):
        """Return True if this XBlock uses custom completion criteria."""
        return True

    display_name = String(
        default="Click Aware XBlock",
        display_name="Component Display Name",
        help="The name students see. This name appears in the course ribbon and as a header for the video.",
        scope=Scope.content,
    )
    description = String(default="Click on this link", scope=Scope.content)
    link_url = String(default="https://www.example.com", scope=Scope.content)
    viewed = Boolean(default=False, scope=Scope.user_state_summary)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the ClickAwareXBlock, shown to students
        when viewing courses.
        """
        context = {
            "i18n_service": self.runtime.service(self, "i18n"),
            "display_name": self.display_name,
            "description": self.description,
            "link": self.link_url,
        }
        frag = Fragment()
        frag.content = render_template("clickaware.html", **context)
        frag.add_css(self.resource_string("static/css/clickaware.css"))
        frag.add_javascript(self.resource_string("static/js/src/clickaware.js"))
        frag.initialize_js("ClickAwareXBlock")
        return frag

    def studio_view(self, context=None):
        context = {
            "i18n_service": self.runtime.service(self, "i18n"),
            "display_name": self.display_name,
            "link": self.link_url,
            "description": self.description,
        }

        frag = Fragment()
        frag.content = render_template("clickaware-studio.html", **context)
        frag.add_css(self.resource_string("static/css/clickaware-studio.css"))
        frag.add_javascript(self.resource_string("static/js/src/clickaware-studio.js"))
        frag.initialize_js("ClickAwareXBlockEdit")
        return frag

    @XBlock.json_handler
    def mark_as_viewed(self, data, suffix=""):
        self.viewed = True
        self.runtime.publish(self, "completion", {"completion": 1.0})
        return {"result": "success"}

    @XBlock.json_handler
    def save_content(self, data, suffix=""):
        self.link_url = data.get("linkVal")
        self.display_name = data.get("displayNameVal")
        self.description = data.get("descriptionVal")
        return {"result": "success"}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            (
                "ClickAwareXBlock",
                """<clickaware/>
             """,
            ),
            (
                "Multiple ClickAwareXBlock",
                """<vertical_demo>
                <clickaware/>
                <clickaware/>
                <clickaware/>
                </vertical_demo>
             """,
            ),
        ]
