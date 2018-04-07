let event = {
  keywords: "",
  tags: [],
  radius: 2,
  user_location: "San Francisco, CA",
  cost: 20,  //upper bound of cost
  time: [],
  date: ""
};

let markers = [];

let map;

$(document).ready(function () {
  // dropdown menu display upon clicking on Event Keywords form area
  $('.event-keywords form').on('click', function () {
    $('.dropdown_tags').show();
  });

  // dropdown menu hidden when user moves the mouse elsewhere
/*
  $('.dropdown_tags').mouseleave(function () {
    $('.dropdown_tags').hide();
  });
*/

  /* Event Keywords Input:
     1. Accept either user keywords or checked event tags.
     2. User keywords may be added at the end of event tags selection, in which
     case the entire input is taken as user keywords.  Event tags will be an
     empty array.
     3. User keywords entered at the beginning or the middle of event tags
     selection will be erased and replaced by the checked event tags.
  */

  // updates query after user presses enter on tag form input
  $('#tags').keypress(function (event) {
    if (event.which == 13) {
      saveKeywords();
    }
  });

  // updates query after user clicks outside form area
  $('#tags').blur(function () {
    // if text input exists, clear all checked event tags
    if (typeof $('#tags').val() != 'undefined') {
      saveKeywords();
    }
  });


  // updates query as user makes event tag selection by clicking on <li>
  $('.dropdown_tags li').click(function () {
    eventTag = this.children[0].dataset.name
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

    console.log(event);
    getEvents();

//    console.log("tags: ", event['tags']);
//    console.log("keywords: ", event['keywords']);

    // display the checked tags in the Keyword search area
    if (event['tags'].length > 0) {
      $('#tags').val(event['tags'].join(', '));
    } else {
      $('#tags').val("");
    }
  });

  // updates query after user inputs search radius
  $('#radius').blur(function () {
    saveRadius();
  });

  // updates query after user presses enter on radius
  $('#radius').keypress(function (event) {
    if (event.which == 13) {
//      console.log("radius submission!");
      saveRadius();
      }
  });

  // updates query as user inputs location
    $('#user_location').blur(function () {
      saveLocation();
    });

  // updates query after user presses enter on location
  $('#user_location').keypress(function (event) {
    if (event.which == 13) {
//      console.log("location submission!");
      saveLocation();
    }
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

  // cost slider hides when user clicks on the Apply button
  // cost button is updated with cost display
  $('#cost-apply').click(function () {
    hideCost();
  });

  // time dropdown apppears when user clicks on the Time button
  $('#time').click(function () {
    $('.hours').show();
  });

  // update query as user makes time selection
  $('.hours li').click(function () {
    timeSlot = this.children[0].dataset.name

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

  // time button is updated with times selected after Apply button is pressed
  $('#time-apply').click(function () {
    hideTime();
  });

  // hides dropdown menu when user clicks outside the menu
  $(document).click(function (event){

    if (!$(event.target).closest('div.event-keywords').length
    && $('.dropdown_tags').is(":visible")) {
      $('ul.dropdown_tags').hide();
    }
    if (!$(event.target).closest('section.event-cost').length
	&& $('.cost-slider').is(":visible")) {
      hideCost();
    }
    if (!$(event.target).closest('div.time').length
       && $('.hours').is(":visible")) {
      hideTime();
    }
  });
  console.log(event);
});

// hides Time dropdown && update button with selected time
function hideTime() {
  $('.hours').hide();
  if (event['time'].length === 3 || event['time'].length === 0) {
    $('#time').text("All Day");
  } else {
    $('#time').text(event['time'].join(', '));
  }
  $('#time').css({"background-color": "#f44271", "color": "white"});

  console.log(event);
  getEvents();
}


// hides Cost dropdown && update button with selected cost
function hideCost() {
  $('.cost-slider').hide();
  event['cost'] = $('#price').text().slice(1);
  $('#cost').text($('#price').text());
  $('#cost').css({"background-color": "#f44271", "color": "white"});

  getEvents();
}


function saveRadius() {
  if (typeof $('#radius').val() != 'undefined') {   // if text input exists
    event['radius'] = $('#radius').val();
    console.log(event['radius']);

    console.log(event);
    getEvents();
  }
}

function saveLocation() {
  if (typeof $('#user_location').val() != 'undefined') {   // if text input exists
    event['user_location'] = $('#user_location').val();
    console.log(event['user_location']);
    getEvents();
  }
}

function uncheckAllTags() {
  $('.dropdown_tags li').each(function () {
    if ($(this).find("input").prop("checked")) {
      $(this).find("input").prop("checked", false);
    }
  });
}

function saveKeywords() {
  if (typeof $('#tags').val() != 'undefined') {
    event['keywords'] = $('form #tags').val();
    event['tags'] = [];

    uncheckAllTags();

    console.log(event);
    getEvents();

//    console.log("keywords:", event['keywords']);
//    console.log("tags: ", event['tags']);
  }
}

// send event object to the backend & query corresponding events
function getEvents() {
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5000/api/event_search',
    contentType: 'application/json',  // type of data sent to the server
    data: JSON.stringify(event),  // data to be sent to the server
    dataType: 'json',  // type of data expected from the server
                       // jquery will auto convert json to JS object
    success: function (data) {
      // remove existing markers
      deleteMarkers();
      // populate page with new event markers
      addMarkers(data);
    }
  });
}

// create markers && add them to the map
function addMarkers(data) {
  // data is a dictionary of events
  // {'id_1': {'cost': 20, 'address': '18th St', ...}, 'id_2': {'cost': 33, ...}}
  let infoWindow = new google.maps.InfoWindow();
  let marker, i;

  // construct marker objects from event data from the server
  for (i = 0; i < Object.keys(data).length; i++) {
    marker = new google.maps.Marker({
      position: new google.maps.LatLng(data[i].location.lat, data[i].location.lon),
      map: map
    });

    markers.push(marker);

    // info window display when marker is clicked
    google.maps.event.addListener(marker, 'click', (function(markerObj, i) {
      return function() {
	infowindow.setContent('<h3><b>' + data[event_key].name + '</b></h3>'
			      + '<p>Address: ' + data[event_key].address + '</p>'
			      + '<p>Date: ' + data[event_key].date + '</p>'
			      + '<p>Time: ' + data[event_key].time + '</p>'
			      + '<p>Tags: ' + data[event_key].tags + '</p>');
	infowindow.open(map, markerObj);
	}
    })(marker, i));
  }
}

// delete all markers
function deleteMarkers() {
  // clear markers from the map
  if (markers.length > 0) {
    for (let marker of markers) {
    marker.setMap(null);
    }
  }
  // remove marker references from the array
  markers = [];
}


// display map
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 37.781715, lng:-122.408367} //Holberton Address. REVISIT
  });
}
