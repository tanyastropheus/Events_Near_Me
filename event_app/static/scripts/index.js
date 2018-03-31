// collect input from all form fields and save them to the event object
//function getAttrs()

// send event object to the backend & query corresponding events
//function getEvents()


let event = {
  keywords: "",
  tags: [],
  radius: 2,
  user_location: "San Francisco, CA",
  cost: 0,  //upper bound of cost
  time: "",
  date: ""
}

$(document).ready(function () {
  // dropdown menu display upon clicking on Event Keywords form area
  $('.event-keywords form').on('click', function () {
    $('.dropdown_tags').show();
  });

  // dropdown menu hidden when user moves the mouse elsewhere
  $('.dropdown_tags').mouseleave(function () {
    $('.dropdown_tags').hide();
  });

  /* Event Keywords Input:
     1. Accept either user keywords or checked event tags.
     2. User keywords may be added at the end of event tags selection, in which
     case the entire input is taken as user keywords.  Event tags will be an
     empty array.
     3. User keywords entered at the beginning or the middle of event tags
     selection will be erased and replaced by the checked event tags.
  */

  // get user keywords input
  $('#tags').blur(function () {
    console.log("blur happened");
    // if text input exists
    if (typeof $('#tags').val() != 'undefined') {
      console.log("some input");
      event['keywords'] = $('form #tags').val();
      event['tags'] = [];

     // uncheck all event tags
      $('.dropdown_tags li').each(function () {
	if ($(this).find("input").prop("checked")) {
	  $(this).find("input").prop("checked", false);
	}
      });

      console.log("keywords:", event['keywords']);
      console.log("tags: ", event['tags']);

      // remove existing pins on the map
      // call getAttrs()
      // call getEvents()
    }
  });

  // get event tags
  // user can click on event tag <li> to check boxes
  $('.dropdown_tags li').click(function () {
    if ($(this).find("input").prop("checked") === false) {
      $(this).find("input").prop("checked", true);

      // add checked tags to array
      event['tags'].push(this.children[0].children[0].dataset.name);
      event['keywords'] = "";  // remove user input from event object

      // remove existing pins on the map
      // call getAttrs()
      // call getEvents()

    } else {
      $(this).find("input").prop("checked", false);

      // remove unchecked tag from the array
      const index = event['tags'].indexOf(this.children[0].children[0].dataset.name);

      if (index !== -1) {
	event['tags'].splice(index, 1);
      }
    }
    // remove existing pins on the map
    // call getAttrs()
    // call getEvents()

    console.log("tags: ", event['tags']);
    console.log("keywords: ", event['keywords']);

    // display the checked tags in the Keyword search area
    if (event['tags'].length > 0) {
      $('#tags').val(event['tags'].join(', '));
    } else {
      $('#tags').val("");
    }
  });

  // get radius
  $('#radius').focus(function () {
    $('#radius').blur(function () {
      if (typeof $('#radius').val() != 'undefined') {   // if text input exists
	event['radius'] = $('#radius').val();
	console.log(event['radius']);
	// remove existing pins on the map
	// call getAttrs()
	// call getEvents()
      }
    });
  });

  // get user location
  $('#user_location').focus(function () {
    $('#user_location').blur(function () {
      if (typeof $('#user_location').val() != 'undefined') {   // if text input exists
	event['user_location'] = $('#user_location').val();
	console.log(event['user_location']);
	// remove existing pins on the map
	// call getAttrs()
	// call getEvents()
      }
    });
  });

  // cost slider appears when user clicks on the cost button
  $('#cost').click(function () {
    $('.cost-slider').show();
  });

  // cost display on the dropdown updates with slider movement
  $( "#cost-range" ).slider({
    range: "min",
    value: 20,
    min: 0,
    max: 100,
    slide: function( event, ui ) {
      if (ui.value === 100) {
	$( "#price" ).text( "$" + ui.value + "+");
	} else {
	  $( "#price" ).text( "$" + ui.value );
	}
    }
  });
  $("#price").text("$" + $( "#cost-range" ).slider( "value" ) );

  // cost slider disappears when user moves mouse away
  // cost button is updated with cost display
  $('.cost-slider').mouseleave(function () {
    $('.cost-slider').hide();
    $('#cost').text($('#price').text());
    $('#cost').css({"background-color": "#f44271", "color": "white"});
    // remove existing pins on the map
    // call getAttrs()
    // call getEvents()
  });

  // time dropdown apppears when user clicks on the Time button
  $('#time').click(function () {
    $('.hours').show();
  });

  // time dropdown disappears when user mouses away
  // time button is updated with user input
  $('.hours').mouseleave(function () {
    $('.hours').hide();
  });

});
