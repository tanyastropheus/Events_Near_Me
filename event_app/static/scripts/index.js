// add slider for radius distance
/*
$(document).ready( function() {
    $( "#slider-range-min" ).slider({
      range: "min",
      value: 37,
      min: 1,
      max: 700,
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.value );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range-min" ).slider( "value" ) );
  } );
*/

// collect input from all form fields and save them to the event object
//function getAttrs()

// send event object to the backend & query corresponding events
//function getEvents()


let event = {}  // event object with attributes (keyword, date, time...) as key
/* event = {keywords: "",  (user input - free text search)
            tags: [], (checked boxes - exact match)
	    cost: 0 (upperbound),
	    time: "",
	    date: ""}
*/
let tags = []

$(document).ready(function() {
  // dropdown menu display upon clicking on Event Keywords form area
  $('.event-keywords form').on('click', function () {
    $('.dropdown_tags').show();
  });

  // retrieving user keywords
  $('li input[type=checkbox]').get(0).focus(function () {
    console.log("in focus!");
    if (typeof $('#tags').val() != 'undefined') {  // if text input exists
      console.log($('#tags').val());
      $('li input[type=checkbox]').blur(function () {
	event[keywords] = $('#tags').val();
	console.log(event);
	// remove existing pins on the map
	// call getAttrs()
	// call getEvents()
      });
    }
  });


  // add event tags to the tags array
  $('li input[type=checkbox]').on('click', function () {
    if (this.checked) {  // add checked tag to the array
      tags.push(this.dataset.name);

      // remove existing pins on the map
      // call getAttrs()
      // call getEvents()

    } else {  // remove unchecked tag from the array
      const index = tags.indexOf(this.dataset.name);
      if (index !== -1) {
	tags.splice(index, 1);
      }

      // remove existing pins on the map
      // call getAttrs()
      // call getEvents()
    }
    console.log(tags);

    // display the checked tags in the Keyword search area
    if (tags.length > 0) {
      $('#tags').val(tags.join(', '));
      } else {
	$('#tags').val("");
      }
  });
});
