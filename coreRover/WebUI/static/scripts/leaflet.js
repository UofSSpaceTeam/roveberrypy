//global variables 
var roverMarker 


//sends all marker coordinates to rover 
function sendMarkers(array) {
	var i;
	$.ajax({
		url: "/testSend",
		type: "POST",
		data: JSON.stringify({"nodes" : array}),
		contentType: "application/json"
	});	
}


/*	
Prints out all maker coordinates in the system
*/
function printMarkers(array) {
	var i;
	var marker = ""; 
	for (i = 0; i < array.length; i++) {
		//printing for testing purposes
		//change to send elements
		marker += "<p>" + array[i] + "</p>";				
	}
	//outputs array
	//document.getElementById("marker_array").innerHTML = marker;	
}

/*
updates the rovers current position 
*/
function updateRoverPos() {
	
	//get Coordinates from input boxes
	//var latlng = L.latLng(document.getElementById("YPos").value, document.getElementById("XPos").value);
	//get coordinates from rover input
	var latlng = L.latLng(document.getElementById("YPos").value, document.getElementById("XPos").value);
	//set new rover position 
	roverMarker.setLatLng(latlng);
	//updates the rovers position 
	roverMarker.update();
}


function main(){
		
		
		//var osmUrl = 'maps/output/{z}/{x}/{y}.png',
		var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
		osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
		
		//osm = L.tileLayer(osmUrl, {maxZoom: 18}),

		
		osm = L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttrib}),
		//TODO:change initial position 
		map = new L.Map('map', {layers: [osm], center: new L.LatLng(52.13100, -106.63400), zoom: 15 });

	var drawnItems = new L.FeatureGroup();
	map.addLayer(drawnItems);
	
	var num = 0;
	var marker_array = [];
	
	//makes roverIcon
	//TODO: the initial position should be changed
	roverMarker = L.marker([52.13, -106.63]).addTo(map);
	roverMarker.bindPopup("I'm the rover!!");
	//set input boxes to initial value
	document.getElementById("XPos").value = -106.63400;
	document.getElementById("YPos").value = 52.13100;
	
	var drawControl = new L.Control.Draw({
		position: 'topright',
		draw: {
			polyline: false,
			polygon: false,
			circle: false,
			rectangle: false, 
			marker: {}
		},
		edit: {
			featureGroup: drawnItems,
			edit: false
		}
	});
	map.addControl(drawControl);

	map.on('draw:created', function (e) {
	
		var type = e.layerType,
			layer = e.layer;
		if (type === 'marker') {
			num++; 
			var latlng = layer.getLatLng();
			message = num.toString().concat(",",latlng.lat, ",",latlng.lng ); 
			layer.bindPopup(message);
			marker_array.push(message); 
			sendMarkers(marker_array);
			//printMarkers(marker_array); 

		}
		drawnItems.addLayer(layer);
	});

	map.on('draw:edited', function (e) {
		var layers = e.layers;
		var countOfEditedLayers = 0;
		layers.eachLayer(function(layer) {
			countOfEditedLayers++;
		});
		console.log("Edited " + countOfEditedLayers + " layers");
	});

	}
