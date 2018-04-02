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
  time: [],
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

  // updates query as user enters event keywords
  $('#tags').blur(function () {
    console.log("blur happened");

    // if text input exists, clear all checked event tags
    // will perform free text search
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

  // updates query as user makes event tag selection by clicking on <li>
  $('.dropdown_tags li').click(function () {
    eventTag = this.children[0].children[0].dataset.name
    if (event['tags'].includes(eventTag) === false) {

      // add checked tags to array
      event['tags'].push(eventTag);
      event['keywords'] = "";  // remove user input from event object

      // checkbox display checked
      $(this).find("input").prop("checked", true);
    } else {

      // remove unchecked tags from the array
      const index = event['tags'].indexOf(eventTag);

      if (index !== -1) {
	event['tags'].splice(index, 1);

	// checkbox display unchecked
	$(this).find("input").prop("checked", false);
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

  // updates query as user makes event tag selections by clicking on the checkbox
  $('.dropdown_tags input[type=checkbox').click(function () {
      console.log("input: ", $(this).prop("checked"));
});


  // updates query as user enters radius to search
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

  // updates query as user enters location
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

  // update map as user makes time selection
  $('.hours li').click(function () {
    timeSlot = this.children[0].children[0].dataset.name

    if (event['time'].includes(timeSlot) === false) {
      // add checked time slot to array
      event['time'].push(timeSlot);

      // checkbox display checked
      $(this).find("input").prop("checked", true);

    } else {
      // remove time slot from array
      const index = event['time'].indexOf(this.children[0].children[0].dataset.name);

      if (index !== -1) {
	event['time'].splice(index, 1);

	// checkbox display unchecked
	$(this).find("input").prop("checked", false);
      }
    }
    console.log(event['time']);
  });

  // time dropdown disappears when user moves mouse away
  // time button is updated with times selected
  $('.hours').mouseleave(function () {
    $('.hours').hide();
    if (event['time'].length === 3 || event['time'].length === 0) {
      $('#time').text("All Day");
    } else {
      $('#time').text(event['time'].join(', '));
    }
    $('#time').css({"background-color": "#f44271", "color": "white"});
    // remove existing pins on the map
    // call getAttrs()
    // call getEvents()
  });
});
