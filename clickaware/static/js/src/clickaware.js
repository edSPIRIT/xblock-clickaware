/* Javascript for ClickAwareXBlock. */
function ClickAwareXBlock(runtime, element) {
  $("#target-url").click(function (e) {
    e.preventDefault();
    {
      $.ajax({
        type: "POST",
        url: runtime.handlerUrl(element, "mark_as_viewed"),
        data: JSON.stringify({}),
        success: function (data) {
          if (data.result === "success") {
            // Handle success or update UI as needed
          }
        },
      });
    }
    // Open href in new window
    window.open(this.href, "_blank");
  });
}
