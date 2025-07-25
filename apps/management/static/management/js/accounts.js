function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submitNewAccount(){
    const name = document.getElementById('new-account-name').value;

    if(!name){
        return;
    }

    fetch('/management/accounts/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({
            'username': name
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Conta criada com sucesso!');
            window.location.reload();
        } else {
            alert('Erro: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });
}

async function toggleAccountStatus(type, id){
    let msg = `Deseja realmente ${type === 'activate' ? 'ativar' : 'desativar'} a conta?`;
    if(confirm(msg)){
        try {
            const response = await fetch('/management/accounts/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    id: id,
                })
            })

            if(!response.ok){
                alert(response.msg);
                return;
            }

            alert('Alteração concluída');
            window.location.reload();
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro na requisição');
        }
    }
    else {
        return;
    }
}