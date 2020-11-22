var MapApp = {};

MapApp.render = function (billData, houseData, senateData) {
    var districts = billData.reduce(function(acc, cur) {
        acc[cur.district] = cur;
        return acc;
    }, {});

    var districtOptions = {
        onEachFeature: function (feature, layer) {
            var district = districts[feature.properties.district];
            layer.bindPopup(
                district.district + '<br>' +
                // TODO: Legislator URL
                district.first_name + ' ' + district.last_name + '<br>'
            );
        },
        style: function (feature) {
            var district = districts[feature.properties.district];
            return {
                className: 'district' + (
                    district.sponsor ? ' district--sponsored' : ''
                )
            };
        },
    };

    var districtLayers = {
        'House': L.geoJson(houseData, districtOptions),
        'Senate': L.geoJson(senateData, districtOptions),
    };

    // TODO: Constrain zoom and bounds
    // TODO: Search
    MapApp.map = L.map('map')
        .addLayer(L.stamenTileLayer('toner-lite'))
        .addLayer(districtLayers['House'])
        .addControl(
            L.control.layers(districtLayers, {}, {
                collapsed: false
            })
        )
        .fitBounds(districtLayers['House'].getBounds());
};

// TODO: https://github.com/github/fetch
// TODO: topojson
Promise.all(
    [
        window.location + '?format=json',
        '/static/ma_house_districts.geojson',
        '/static/ma_senate_districts.geojson',
    ]
    .map(function (url) {
        return fetch(url)
            .then(function (response) { return response.json(); });
    })
).then(function (allData) {
    MapApp.render.apply(null, allData);
});
