function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

function associateAccount(id){
    const btn = document.getElementById(`account-btn-${id}`);
    if (btn) {
        btn.classList.toggle('active');
    }
}

async function submitNewUser(){
    const name = document.getElementById('new-name').value;
    const email = document.getElementById('new-email').value;
    const password = document.getElementById('new-password').value;

    if(!name || !email || !password){
        alert('Preencha os dados corretamente.');
        return;
    }

    const selectedAccounts = document.querySelectorAll('.account-btn.active');

    const accounts = Array.from(selectedAccounts).map(account => {
        return {
            id: account.id.replace('account-btn-', ''),
            name: account.textContent.trim()
        };
    });

    try {
        const response = await fetch('/management/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password,
                accounts: accounts,
            })
        })

        if(!response.ok){
            alert(response.msg);
            return;
        }

        alert('Usuario adicionado!');
        window.location.reload();
    } catch (error) {
        alert('Erro na requisição');
    }
    
}