
/**
 * Elements that make up the popup.
 */
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');
/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
closer.onclick = function() {
    overlay.setPosition(undefined);
    closer.blur();
    return false;
};
/**
 * Create an overlay to anchor the popup to the map.
 */
var overlay = new ol.Overlay({
    element: container,
    autoPan: true,
    autoPanAnimation: {
        duration: 250
    }
});


var map = new ol.Map({
    target: 'map',
    overlays: [overlay],
    layers: [
        new ol.layer.Tile({source: new ol.source.OSM()
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([29.07, 41.05]),
        zoom: 11
    })
});

var features = [];
for ( pos in stops ) {
    var row = stops[pos];var latitude = row[1];
    var longitude = row[2];
    var iconFeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857')),
        name: row[0]
    });
    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(({
            anchor: [0.5, 1],
            src: "https://mapmarker.io/api/v2/font-awesome/v5/pin?size=25&color=FFF&hoffset=0&voffset=0"
        }))
    });
    iconFeature.setStyle(iconStyle);
    features.push(iconFeature);
}
for ( pos in buses ) {	    var row = buses[pos];var latitude = row[1];	    var longitude = row[2];	    var iconFeature = new ol.Feature({	    geometry: new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857')),	    name: row[0]	});	    var iconStyle = new ol.style.Style({	    image: new ol.style.Icon(({	        anchor: [0.5, 1],	        src: "https://mapmarker.io/api/v3/font-awesome/v6/icon?icon=fa-solid%20fa-bus-simple&size=25&color=2d3748"	}))	});	    iconFeature.setStyle(iconStyle);	    features.push(iconFeature);	}	var vectorSource = new ol.source.Vector({	    features: features	});	var vectorLayer = new ol.layer.Vector({	    source: vectorSource	});map.addLayer(vectorLayer);/**
 * Add a click handler to the map to render the popup.
 */
map.on('singleclick', function(evt) {
    var name = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
        return feature.get('name');
    })
    if (name) {
        container.style.display="block";
        var coordinate = evt.coordinate;
        content.innerHTML = name;
        overlay.setPosition(coordinate);
    } else {
        container.style.display="none";
    }
});
map.on('pointermove', function(evt) {
    map.getTargetElement().style.cursor = map.hasFeatureAtPixel(evt.pixel) ? 'pointer' : '';
});		/* http://www.geocodezip.com/OL_5.3.0_simpleMultipleMarkerExample.html */	/* https://openlayers.org/ */
