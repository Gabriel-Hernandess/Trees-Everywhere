function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

async function submitNewTree(){
    if(!confirm('Deseja realmente adicionar a árvore?')){
        return;
    }

    const name = document.getElementById('new-name').value;
    const scientificName = document.getElementById('new-scientific-name').value;

    if(!name || !scientificName){
        alert('Preencha os dados corretamente');
        return;
    }
    
    try {
        const response = await fetch('/management/trees/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                name: name,
                scientificName: scientificName
            })
        });

        if (!response.ok) {
            alert('Erro ao adicionar planta, tente novamente.');
            return;
        }

        alert('Planta adicionada com sucesso.');
        window.location.reload();
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro ao adicionar planta.');
    }
}

function openPlanted(id) {
    console.log(id);
    const el = document.getElementById(`planted-${id}`);
    if (el) {
        el.style.display = 'flex';
    }
}

function closePlanted(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.display = 'none';
    }
}

let mapInstances = {};
let markerInstances = {};

function initMap(lat, lng, mapId) {
    const mapEl = document.getElementById(mapId);
    if (!mapEl) return;

    mapInstances[mapId] = L.map(mapEl).setView([lat, lng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © OpenStreetMap contributors',
    }).addTo(mapInstances[mapId]);
}

function showOnMap(lat, lng, mapId) {
    if (!mapInstances[mapId]) {
        initMap(lat, lng, mapId);
    } else {
        mapInstances[mapId].setView([lat, lng], 15);
    }

    if (markerInstances[mapId]) {
        markerInstances[mapId].setLatLng([lat, lng]);
    } else {
        markerInstances[mapId] = L.marker([lat, lng]).addTo(mapInstances[mapId]);
    }
}