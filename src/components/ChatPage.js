import React from 'react';
import ScriptTag from "react-script-tag";
import { useEffect } from 'react';
import axios from "axios";
import { useParams } from 'react-router';
import PersonIcon from '@material-ui/icons/Person';



export default function ChatPage() {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('X-CSRFToken');

    const { roomname } = useParams();

    async function ChatPageManager() {
        let response = await fetch('/roomavailable', {
            credentials: 'include',
            method: 'POST',
            mode: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'rname': roomname
            })
        })
        if (response.ok) {
            let json = await response.json();
            let message = json["message"]
            if (message != 'success')
                window.location.replace('/chat')
        }
        else {
            alert("HTTP-Error: " + response.status);
        }
    }

    ChatPageManager()

    useEffect(() => {
        axios.get('/auth/isauth')
            .then(res => {
                if (!res['data']['message']) {
                    window.location.replace('/login')
                }
            })
            .catch(err => {
                alert(err)
            })
    })






    return (
        <>
            <div className="upperpart">
                <h3 id="groupname">Group: </h3>
                <h5 id="username">User: </h5>
                <div className="managericonum">
                    <PersonIcon className="personico" />
                    <h6 id="activepersons"></h6>
                </div>
            </div>
            <div id="chat-log"></div><br />
            <div className="flexcontainer">
                <textarea id="chat-message-input" required type="text" cols="150" rows="3"></textarea><br />
                <input id="chat-message-submit" type="button" value="Send" />
            </div>
            <ScriptTag src="/public/chatserver.js"></ScriptTag>
        </>
    )
}
