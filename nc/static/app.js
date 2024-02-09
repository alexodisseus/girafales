 $(function() {
    $(".draggable-card").draggable({
      stack: ".draggable-card",
      revert: true
    });

    $(".draggable-card").droppable({
      drop: function(event, ui) {
        var draggedText = ui.draggable.find(".card-text").text();
        var targetText = $(this).find(".card-text").text();
        $(this).find(".card-text").text(targetText + " " + draggedText);
        ui.draggable.remove();
      }
    });
  });