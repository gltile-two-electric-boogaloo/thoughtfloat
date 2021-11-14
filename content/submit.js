const FUCKFUCKF = (token) => {
    if (document.getElementById("input").value.length == 0) {
        document.getElementById("errormessage").innerText = "No content."
        return
    } else if (document.getElementById("input").value.length > 240) {
        document.getElementById("errormessage").innerText = "Content exceeds 240 characters."
        return
    }
    let xhr = new XMLHttpRequest()

    xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status != 200) {
                document.getElementById("errormessage").innerText = JSON.parse(xhr.responseText)['detail']
            } else {
                location.reload()
            }
        }
    }

    xhr.open('POST', "/api/v1/thoughts")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(JSON.stringify({
        "content": document.getElementById("input").value,
        "recaptcha_token": token
    }))
}

window.FUCKFUCKF = FUCKFUCKF