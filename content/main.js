document.getElementById("input").addEventListener('input', () => {
    document.getElementById("charcount").innerText = `${document.getElementById("input").value.length}/240`
})

let xhr = new XMLHttpRequest()

xhr.onreadystatechange = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) { 
        if (xhr.status == 200) {
            JSON.parse(xhr.responseText).forEach((m) => {
                document.getElementById("thoughts").innerHTML = `
                <div class="thought-container">
                    <div class="thought">
                        <h4>${new Date(m['last_updated']).toTimeString()}</h4>
                        <p>${m['content']}</p>
                    </div>
                </div>` + document.getElementById("thoughts").innerHTML
            })
        }
    }
}

xhr.open('GET', '/api/v1/thoughts')
xhr.send('')