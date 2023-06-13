
const username = localStorage.blogUsername? localStorage.blogUsername : ""

if(username == "") {
    window.location.href = "/login";
}

document.querySelector("#username").innerHTML = `¡Hola ${username}!`;

document.querySelector("#salir").onclick = () => {
    localStorage.blogUsername = "";
    window.location.href = "/login";
}

const url = `/api/v1.0/posteos`

document.querySelector("#publicar").onclick = async () => {
    let formData = new FormData();
    const titulo = document.querySelector("#titulo").value;
    const texto = document.querySelector("#texto").value;
    
    const data = {
        titulo: titulo,
        texto: texto,
    }
    
    fetch(`${url}/${username}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if(response.ok) {
             window.location.reload(true)
        }
        else {
            alert(response.statusText)
        }
    })
    .catch(error => console.error('Error:', error))
}


fetch(`${url}/${username}`)
    .then(response => response.json())
    .then(posts => {
        let accumulator = ""

        // Leer los últimos elementos primero:
        const reversedArray = posts.reverse();

        // Solo leer los últimos 3 elementos
        reversedArray.slice(0, 3).forEach(post => {
            accumulator += 
                `
                <div>
                    <p id="titulo">${post.titulo}</p>
                    <p id="texto">${post.texto}</p>
                    <hr>
                </div>
                `
        });
        const section = document.querySelector("#posteos");
        section.innerHTML = accumulator;
    })

