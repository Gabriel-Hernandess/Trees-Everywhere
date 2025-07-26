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

function openPlanted(id){
    const div = document.getElementById(`planted-${id}`);
    div.style.display = 'flex';
}

let mapInstance = null;
let markerInstance = null;

function initMap(lat, lng) {
    const mapEl = document.getElementById('map');
    if (!mapEl) return;

    // Cria o mapa uma única vez
    mapInstance = L.map(mapEl).setView([lat, lng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © OpenStreetMap contributors',
    }).addTo(mapInstance);
}

function showOnMap(lat, lng) {
    if (!mapInstance) {
        initMap(lat, lng);
        return;
    }

    // Move o mapa para nova posição
    mapInstance.setView([lat, lng], 15);

    // Move o marcador
    if (markerInstance) {
        markerInstance.setLatLng([lat, lng]);
    } else {
        markerInstance = L.marker([lat, lng]).addTo(mapInstance);
    }
}


function closePlanted(){
    document.querySelector('.planted-tree-list').style.display = 'none';
}