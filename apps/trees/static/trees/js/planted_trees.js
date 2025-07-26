function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

let map;
let marker = null;
let plantedTrees = [];

window.onload = () => {
    initMap();
};

function initMap() {
    map = L.map('map').setView([-23.5505, -46.6333], 13); // São Paulo como exemplo

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    map.on('click', function (e) {
        if (marker) map.removeLayer(marker);

        marker = L.marker(e.latlng).addTo(map);
        marker.coords = e.latlng;
    });
}

function addPlantedTree() {
    const treeSelect = document.getElementById('tree-select');
    const treeId = treeSelect.value;
    const treeName = treeSelect.options[treeSelect.selectedIndex].text;

    const accountSelect = document.getElementById('account-select');
    const accountName = accountSelect.options[accountSelect.selectedIndex].text;
    const accountId = accountSelect.value;

    const newPlantedList = document.querySelector('.new-planted-list div');

    if (!marker) {
        alert('Por favor, selecione uma localização no mapa.');
        return;
    }

    plantedTrees.push({
        tree_id: treeId,
        lat: marker.getLatLng().lat,
        lng: marker.getLatLng().lng,
        name: treeName,
        account: accountId
    });

    const newElement = document.createElement('p');
    newElement.textContent = `${treeName}, ${accountName} | (${marker.getLatLng().lat}, ${marker.getLatLng().lng})`;
    newPlantedList.appendChild(newElement);

    map.removeLayer(marker);
    marker = null;
}

function submitPlantedTrees() {
    if (plantedTrees.length === 0) {
        alert('Nenhuma árvore adicionada.');
        return;
    }

    fetch('/trees/planted-trees/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ trees: plantedTrees })
    }).then(res => {
        if (!res.ok) throw new Error('Erro');
        alert('Árvores salvas com sucesso!');
        window.location.reload();
    }).catch(() => {
        alert('Erro ao salvar árvores.');
    });
}
