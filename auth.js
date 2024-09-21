function handleCredentialResponse(response) {
    fetch('/auth/google', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: response.credential }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('userName').textContent = data.user.name;
            document.getElementById('userInfo').style.display = 'block';
            document.getElementById('googleSignInButton').style.display = 'none';
        } else {
            console.error('Authentication failed:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

window.onload = function () {
    fetch('/get-google-client-id')
        .then(response => response.json())
        .then(data => {
            google.accounts.id.initialize({
                client_id: data.clientId,
                callback: handleCredentialResponse
            });
            google.accounts.id.renderButton(
                document.getElementById("googleSignInButton"),
                { theme: "outline", size: "large" }
            );
            google.accounts.id.prompt();
        })
        .catch(error => console.error('Error:', error));
};

document.getElementById('signOutButton').addEventListener('click', function() {
    document.getElementById('userInfo').style.display = 'none';
    document.getElementById('googleSignInButton').style.display = 'block';
    google.accounts.id.disableAutoSelect();
});


