function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

async function saveAbout(){
    const msgElement = document.getElementById('msg');
    const about = document.getElementById('about').value;

    if(!about){
        alert('Insira uma bio válida');
        return;
    }

    try {
        const response = await fetch('/trees/my-profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ about: about })
        })

        if(response.ok){
            alert('Bio editada com sucesso!');
            window.location.reload();
        }

        else {
            const data = await response.json();
            msgElement.textContent = data.msg || 'Erro ao editar bio.';
        }
    } catch (error) {
        alert('Erro ao editar bio.');

        msgElement.textContent = 'Ocorreu um erro inesperado.';
        console.error(error);
    }
}