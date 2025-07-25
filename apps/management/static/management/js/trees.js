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