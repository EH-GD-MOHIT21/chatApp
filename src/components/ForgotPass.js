import React, { useState } from 'react';
import axios from "axios";
import Spinner from '../muicomp/spinner';
import { useEffect } from 'react';

export default function ForgotPass() {

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


    function handleGT(e) {
        e.preventDefault();
        document.getElementById('spinnerhandler').style.display = 'flex';
        document.getElementById("verifier").textContent = ''
        axios.post('/auth/generateResetToken', {
            'email': document.getElementById('fpemailsec').value,
        })
            .then(res => {
                document.getElementById('spinnerhandler').style.display = 'none';
                document.getElementById('verifier').style.display = 'block';
                if (res['data']['message'] != 'Recovery Option Send on mail.') {
                    document.getElementById("verifier").textContent = res['data']['message'];
                    document.getElementById("verifier").style.color = "crimson"
                    document.getElementById("verifier").style.fontWeight = 600;
                } else {
                    document.getElementById("verifier").textContent = res['data']['message'];
                    document.getElementById("verifier").style.color = "green"

                    document.getElementById("verifier").style.fontWeight = 600;
                }
                return true;
            })
            .catch(err => {
                document.getElementById('spinnerhandler').style.display = 'none';
                alert(err);
            });
    }
    return (
        <div className="ForgotPassContainer">
            <div className="upperfpass">Recovery Password</div>
            <div className="lowerfpass">
                <form action="" onSubmit={(e) => { handleGT(e) }}>
                    <input type="email" placeholder="Enter Registered Email" name="" id="fpemailsec" />
                    <span id="verifier"></span>
                    <Spinner/>
                    <button>Generate Token</button>
                    <a href="/login">Remember Password?</a>
                </form>
            </div>
        </div>
    )
}
