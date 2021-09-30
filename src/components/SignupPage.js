import React, { useState ,useEffect} from 'react';
import { Link } from 'react-router-dom';
import axios from "axios";
import Spinner from '../muicomp/spinner';

export default function SignupPage() {

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

    const [usingotp, setusingotp] = useState(false);
    function handleSubmit(e) {
        e.preventDefault();
        document.getElementById("verifier").textContent = '';
        document.getElementById('spinnerhandler').style.display = 'flex';
        if (!usingotp) {
            axios.post('/auth/register', {
                'fname': document.getElementById('firstnamer').value,
                'lname': document.getElementById('lastnamer').value,
                'email': document.getElementById('emailr').value,
                'phoneno': document.getElementById('phoner').value,
                'password': document.getElementById('passr').value,
                'cpassword': document.getElementById('cpassr').value,
            })
                .then(res => {
                    document.getElementById('spinnerhandler').style.display = 'none';
                    document.getElementById('verifier').style.display = 'block';
                    if (res['data']['message'] != 'otp send on mailid.') {
                        document.getElementById("verifier").textContent = res['data']['message'];
                        document.getElementById("verifier").style.color = "crimson"
                        document.getElementById("verifier").style.fontWeight = 600;
                    } else {
                        document.getElementById('otpregister').style.display = "block";
                        document.getElementById("verifier").textContent = res['data']['message'];
                        document.getElementById("verifier").style.color = "green"
                        setusingotp(true);
                        document.getElementById("verifier").style.fontWeight = 600;
                    }
                    return true;
                })
                .catch(err => {
                    document.getElementById('spinnerhandler').style.display = 'none';
                    alert(err);
                });
        }
        else{
            axios.post('/auth/register/verify', {
                'email': document.getElementById('emailr').value,
                'otp':document.getElementById('otpregister').value
            })
                .then(res => {
                    document.getElementById('spinnerhandler').style.display = 'none';
                    document.getElementById('verifier').style.display = 'block';
                    if (res['data']['message'] != 'success') {
                        document.getElementById("verifier").textContent = res['data']['message'];
                        document.getElementById("verifier").style.color = "crimson"
                        document.getElementById("verifier").style.fontWeight = 600;
                    } else {
                        document.getElementById('otpregister').style.display = "block";
                        document.getElementById("verifier").textContent = res['data']['message'];
                        document.getElementById("verifier").style.color = "green"
                        document.getElementById("verifier").style.fontWeight = 600;
                        window.location.replace(`/chat`)
                    }
                    return true;
                })
                .catch(err => {
                    document.getElementById('spinnerhandler').style.display = 'none';
                    alert(err);
                });
        }
    }
    return (
        <div className="signupcontainer">
            <div className="signupheader">
                <div className="signupupper">
                    <Link to="/login" disabled>Login</Link>
                    <Link to="/signup">Signup</Link>
                </div>
                <div className="signuplower">
                    <form action="" id="SignRegForm" onSubmit={(e) => { handleSubmit(e) }}>
                        <input placeholder="First Name" type="text" id="firstnamer" />
                        <input placeholder="Last Name" type="text" id="lastnamer" />
                        <input placeholder="Enter Email" type="email" id="emailr" />
                        <input placeholder="Enter Number" type="number" id="phoner" />
                        <input placeholder="Enter Password" type="password" id="passr" />
                        <input placeholder="Enter RePassword" type="password" id="cpassr" />
                        <input type="number" id="otpregister" placeholder="Enter OTP" />
                        <span id="verifier"></span>
                        <Spinner/>
                        <button type="submit">Verification</button>
                    </form>
                </div>
            </div>

        </div>
    )
}
