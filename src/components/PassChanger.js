import React from 'react';
import axios from "axios";
import { useParams } from 'react-router';
import Spinner from '../muicomp/spinner';
import { useEffect } from 'react';

export default function PassChanger() {

    useEffect(()=>{
        axios.get('/auth/isauth')
        .then(res=>{
            if(res['data']['message']){
                window.location.replace('/login')
            }
        })
        .catch(err=>{
            alert(err)
        })
    })

    const { user, token } = useParams();

    function handlesubmit(e) {
        e.preventDefault();
        document.getElementById("verifier").textContent = '';
        document.getElementById('spinnerhandler').style.display = 'flex';
        axios.post('/auth/validateFPR/user=' + user + '/token=' + token, {
            'password': document.getElementById('cpnpass').value,
            'cpassword': document.getElementById('cpnrepass').value
        })
            .then(res => {
                document.getElementById('spinnerhandler').style.display = 'none';
                document.getElementById('verifier').style.display = 'block';
                if (res['data']['message'] != 'Success') {
                    document.getElementById("verifier").textContent = res['data']['message'];
                    document.getElementById("verifier").style.color = "crimson"
                    document.getElementById("verifier").style.fontWeight = 600; 
                } else {
                    document.getElementById("verifier").textContent = res['data']['message'];
                    document.getElementById("verifier").style.color = "green"
                    document.getElementById("verifier").style.fontWeight = 600;
                    // redirect to url 'chat'
                    window.location.replace(`/login`)
                }
                return true;
            })
            .catch(err => {
                document.getElementById('spinnerhandler').style.display = 'none';
                alert(err);
            });
    }
    return (
        <div className="passchangerContainer">
            <div className="headerpasschanger">Password Recovery</div>
            <div className="lowerpasschanger">
                <form action="" onSubmit={(e) => { handlesubmit(e) }}>
                    <input type="password" id="cpnpass" placeholder="Enter New Password" />
                    <input type="password" id="cpnrepass" placeholder="ReEnter Password" />
                    <Spinner/>
                    <span id="verifier"></span>
                    <a href="/login">Go to Login</a>
                    <button>Change Password</button>
                </form>
            </div>
        </div>
    )
}
