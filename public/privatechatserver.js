let url = document.URL

async function DealUser() {
    let response = await fetch('/auth/getusername', {
        credentials: 'include',
        method: 'GET',
        mode: 'same-origin'
    })

    if (response.ok) {
        let json = await response.json();
        username = json["message"]
        fullname = json["fullname"]
        if (username == 'Invalid Request.') {
            window.location.replace('/chat')
        } else {
            console.log("logged in as : " + username)
            document.getElementById('username').textContent += username
        }
    } else {
        window.location.replace('/chat')
        alert("HTTP-Error: " + response.status);
    }
}

alignright = false
DealUser()


let RelativeURL = document.URL.split('/')

const roomName = RelativeURL[RelativeURL.length - 1];

document.getElementById('groupname').innerText += ("private " + roomName);

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/private/' +
    roomName +
    '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const activeusers = data.number_of_users
    document.getElementById('activepersons').textContent = activeusers;
    try {
        if (data.username == username)
            alignright = true
        else
            alignright = false
    } catch (err) {
        console.log()
    }
    // managing left and joined grp messages
    if (!data.ext) {
        if (!alignright) {
            document.querySelector('#chat-log').innerHTML += (
                '<div class="newmessage">' + '<div class="username alignleft">' + (data.user + " :" + '\n') + '</div>' + '<div class="message alignleft">' + (data.message + '\n') + '</div>' + '</div>'
            )
        } else {
            document.querySelector('#chat-log').innerHTML += (
                '<div class="rightablecontent">' + '<div class="sendnewmessage">' + '<div class="username alignright">' + (data.user + " :" + '\n') + '</div>' + '<div class="message alignright">' + (data.message + '\n') + '</div>' + '</div>' + '</div>'
            )
        }
    } else {
        document.querySelector('#chat-log').innerHTML += '<div class="message specialgrpmessage">' + (data.message + '\n') + '</div>';
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) { // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    try {
        const xyz = username
    } catch (err) {
        return
    }
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};