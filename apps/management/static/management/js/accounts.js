function getAccounts(){
    fetch('/api/accounts/')
        .then(response => response.json())
            .then(data => {
                console.log('Contas:', data);

        data.forEach(user => {
            const li = document.createElement('li');
            li.textContent = user.nome;
            document.getElementById('accounts-list').appendChild(li);
        });
    });
}