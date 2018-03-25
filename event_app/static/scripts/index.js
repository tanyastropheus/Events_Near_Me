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


let event = {
  keywords: "",
  tags: [],
  cost: 0,  //upper bound of cost
  time: "",
  date: ""
}

$(document).ready(function () {
  // dropdown menu display upon clicking on Event Keywords form area
  $('.event-keywords form').on('click', function () {
    $('.dropdown_tags').show();
  });

  /* 1. Accept either user keywords or checked event tags.
     2. User keywords may be added at the end of event tags selection, in which
     case the entire input is taken as user keywords.  Event tags will be an
     empty array.
     3. User keywords entered at the beginning or the middle of event tags
     selection will be erased and replaced by the checked event tags.
  */

  // get user keywords input
  $('form #tags').focus(function () {
    $('form #tags').blur(function () {
      if (typeof $('#tags').val() != 'undefined') {   // if text input exists
	event['keywords'] = $('form #tags').val();
	event['tags'] = [];
	console.log(event['keywords']);
	console.log(event['tags']);
	// remove existing pins on the map
	// call getAttrs()
	// call getEvents()
      }
    });
  });

  // get event tags
  $('li input[type=checkbox]').on('click', function () {
    if (this.checked) {  // add checked tag to the array
      event['tags'].push(this.dataset.name);
      event['keywords'] = "";  // remove user input from event object
      // remove existing pins on the map
      // call getAttrs()
      // call getEvents()

    } else {  // remove unchecked tag from the array
      const index = event['tags'].indexOf(this.dataset.name);
      if (index !== -1) {
	event['tags'].splice(index, 1);
      }

      // remove existing pins on the map
      // call getAttrs()
      // call getEvents()
    }
    console.log(event['tags']);
    console.log(event['keywords']);
    // display the checked tags in the Keyword search area
    if (event['tags'].length > 0) {
      $('#tags').val(event['tags'].join(', '));
      } else {
	$('#tags').val("");
      }
  });
});
