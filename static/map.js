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
                '<a href="' + district.url + '">' +
                district.first_name + ' ' + district.last_name +
                '</a><br>'
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

    var chamber = window.location.pathname.includes('/S') ? 'Senate': 'House';

    // TODO: Constrain zoom and bounds
    // TODO: Search
    MapApp.map = L.map('map')
        .addLayer(L.stamenTileLayer('toner-lite'))
        .addLayer(districtLayers[chamber])
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
        'https://bhrutledge.com/ma-legislature/dist/ma_house.geojson',
        'https://bhrutledge.com/ma-legislature/dist/ma_senate.geojson',
    ]
    .map(function (url) {
        return fetch(url)
            .then(function (response) { return response.json(); });
    })
).then(function (allData) {
    MapApp.render.apply(null, allData);
});
