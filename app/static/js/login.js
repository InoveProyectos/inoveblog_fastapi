document.querySelector("#ingresar").onclick = async () => {
    const usuario = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

    if(usuario == "" ) {   
        alert("Indique su usuario");
        return;
    }
    if(password == "" ) {   
        alert("Indique la contraseña");
        return;
    }

    let formData = new FormData();
    const url = "/api/v1.0/login";
    
    formData.append("usuario", usuario);
    formData.append("password", password);
    
    fetch(url, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if(response.ok) {
            localStorage.blogUsername = usuario
            window.location.href = "/";
        }
        else {
            alert(response.statusText)
        }
    }
    )
    .catch(error => console.error('Error:', error))

}

document.querySelector("#username").onkeypress = (e) => {
    // Si el usuario presionó "enter"
    // ejecutar la rutina del boton
    if (e.key === "Enter") {
        // Cancel the default action, if needed
        e.preventDefault();
        // Trigger the button element with a click
        document.querySelector("#ingresar").click();
      }   
};

document.querySelector("#password").onkeypress = (e) => {
    // Si el usuario presionó "enter"
    // ejecutar la rutina del boton
    if (e.key === "Enter") {
        // Cancel the default action, if needed
        e.preventDefault();
        // Trigger the button element with a click
        document.querySelector("#ingresar").click();
      }   
};
