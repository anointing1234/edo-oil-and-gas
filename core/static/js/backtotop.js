(function ($) {
  "use strict";

  // Wait for DOM to be fully loaded
  $(document).ready(function () {
    // Get the SVG path element
    var path = document.querySelector(".progress-wrap path");

    // Only proceed if the path element exists
    if (path) {
      var length = path.getTotalLength();

      // Set initial styles
      path.style.transition = path.style.WebkitTransition = "none";
      path.style.strokeDasharray = length + " " + length;
      path.style.strokeDashoffset = length;

      // Force a reflow
      path.getBoundingClientRect();

      // Set transition
      path.style.transition = path.style.WebkitTransition =
        "stroke-dashoffset 10ms linear";

      // Update progress on scroll
      function updateProgress() {
        var scrollTop = $(window).scrollTop();
        var docHeight = $(document).height() - $(window).height();
        var progress = length - (scrollTop * length) / docHeight;
        path.style.strokeDashoffset = progress;
      }

      // Initial update
      updateProgress();

      // Update on scroll
      $(window).scroll(updateProgress);
    }

    // Show/hide button based on scroll position
    $(window).scroll(function () {
      if ($(this).scrollTop() > 50) {
        $(".progress-wrap").addClass("active-progress");
      } else {
        $(".progress-wrap").removeClass("active-progress");
      }
    });

    // Scroll to top on click
    $(".progress-wrap").on("click", function (e) {
      e.preventDefault();
      $("html, body").animate(
        {
          scrollTop: 0,
        },
        550
      );
      return false;
    });
  });

  // Theme switcher (if needed)
  $(".switch").on("click", function () {
    if ($("body").hasClass("light")) {
      $("body").removeClass("light");
      $(".switch").removeClass("switched");
    } else {
      $("body").addClass("light");
      $(".switch").addClass("switched");
    }
  });
})(jQuery);
