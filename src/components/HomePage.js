import React from 'react';
import {
    Link
  } from "react-router-dom";


import { useEffect } from 'react';
import axios from "axios";


export default function HomePage() {

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

    return (
        <div className="homecontainer">
            <div className="headerhome">ChatApp.com</div>
            <div className="cardhome">
                <div className="upper">
                    <h3>Welcome User to Chat App</h3>
                </div>
                <div className="lower">
                    <Link to="/login">Login</Link>
                    <Link to="/signup">Signup</Link>
                </div>
            </div>
        </div>
    )
}
