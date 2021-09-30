import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from "axios";
import Spinner from '../muicomp/spinner';

export default function LoginPage() {

    useEffect(()=>{
        axios.get('/auth/isauth')
        .then(res=>{
            if(res['data']['message']){
                window.location.replace('/chat')
            }
        })
        .catch(err=>{
            alert(err)
        })
    })

    function handleSubmit(e){
        document.getElementById('spinnerhandler').style.display = 'flex';
        e.preventDefault();
        axios.post('/auth/login', {
            'username':document.getElementById('username').value,
            'password':document.getElementById('password').value
        })
        .then(res => {
            document.getElementById('spinnerhandler').style.display = 'none';
            document.getElementById('verifier').style.display = 'block';
            if(res['data']['message']!='success'){
                document.getElementById("verifier").textContent = res['data']['message'];
                document.getElementById("verifier").style.color = "crimson"
                document.getElementById("verifier").style.fontWeight = 600;
            }else{
                document.getElementById("verifier").textContent = res['data']['message'];
                document.getElementById("verifier").style.color = "green"
                document.getElementById("verifier").style.fontWeight = 600;
                window.location.replace(`/chat`)
            }
            return true;
        })
        .catch(err =>{
            document.getElementById('spinnerhandler').style.display = 'none';
            alert(err);
        });
    }
    return (
        <div className="logincontainer">
            <div className="card">
                <div className="upperheaderlogin">
                    <Link to="/login" disabled>Login</Link>
                    <Link to="/signup">Signup</Link>
                </div>
                <div className="lowerheaderlogin">
                    <form action="" onSubmit={(e)=>{handleSubmit(e)}}>
                        <input type="text" placeholder="Enter Email Address" name="" id="username" />
                        <input type="password" placeholder="Enter Password" name="" id="password" />
                        <span id="verifier"></span>
                        <Link to="/forgotpass">Forgot Password?</Link>
                        <Spinner/>
                        <button type="submit">Login</button>
                    </form>
                </div>
            </div>
        </div>
    )
}
