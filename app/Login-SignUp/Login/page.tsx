"use client";
import { BiSolidLockAlt } from "react-icons/bi"
import { IoMdPerson } from "react-icons/io";
import React, { useState, ChangeEvent } from 'react';


import SignUp from "../SignUp/page";

const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleUsernameChange = (event: ChangeEvent<HTMLInputElement>) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
    };

    const login = async () => {
        alert("Logging in...");
        const response = await fetch("http://51.20.249.252:8000/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "username": "admin",
                "password": "admin"
            }),
        });
        alert(response);
        if (response.ok) {
            const data = await response.json();
            alert(data);
        } else {
            alert('Failed to fetch data');
        }

        // const axios = require('axios');
        // let data = JSON.stringify({
        //     "username": "admin",
        //     "password": "admin"
        // });

        // let config = {
        //     method: 'post',
        //     maxBodyLength: Infinity,
        //     url: 'http://51.20.249.252:8000/login',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     data: data
        // };
        // alert("hello");
        // axios.request(config)
        //     .then((response: {data:any}) => {
        //         alert(JSON.stringify(response.data));
        //     })
        //     .catch((error: {data:any}) => {
        //         alert(error);
        //     });
        //     alert("login success");
        // const requestOptions = {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({ username, password })
        // };
        // alert("hello");
        // var request = require('request');
        // var options = {
        //   'method': 'POST',
        //   'url': 'http://51.20.249.252:8000/login',
        //   'headers': {
        //     'Content-Type': 'application/json'
        //   },
        //   body: JSON.stringify({
        //     "username": "admin",
        //     "password": "admin"
        //   })

        // };
        // request(options, function (error, response) {
        //   if (error) throw new Error(error);
        //   alert(response.body);
        // });

        // try {
        //     var myHeaders = new Headers();
        //     myHeaders.append("Content-Type", "application/json");

        //     var raw = JSON.stringify({
        //         "username": "admin",
        //         "password": "admin"
        //     });

        //     var requestOptions = {
        //         method: 'POST',
        //         headers: myHeaders,
        //         body: raw,
        //         redirect: 'follow'
        //     };

        //     fetch("http://51.20.249.252:8000/login", requestOptions)
        //         .then(response => response.text())
        //         .then(result => alert(result))
        //         .catch(error => alert(error));


        //   const response = await fetch('http://51.20.249.252:8000/login', requestOptions);
        //   if (!response.ok) {
        //     const errorData = await response.json();
        //     console.error('API response error:', errorData);
        //     return;
        //   }
        //   const data = await response.json();
        //   alert(data);
        //   console.log(data);
        // }
        //  catch (error) {
        //     alert(error);
        //     console.error('API request error:', error);
        // }
    };

    const goToSignUp = () => {
        window.location.href = '../SignUp/page';
    };


    return (
        <main className="flex flex-col items-center justify-center min-h-screen">
            <div className="bg-white rounded-2xl shadow-md flex w-2/3 max-w-4xl text-center">
                <div className="w-3/5 p-5">
                    <div className="text-left px-4 font-black">
                        <p>CompanyName</p>
                    </div>
                    <div className="py-10">
                        <h2 id="text"
                            className="font-extrabold text-3xl"
                        >Login To Your Account</h2>
                    </div>
                    <div className="flex flex-col align-items-center items-center">

                        <div className="bg-gray-100 flex items-center w-64 p-2 mb-3">
                            <IoMdPerson className="text-gray-400 m-2" />
                            <input type="username" name="username" placeholder="Username" className="bg-gray-100 outline-none text-sm flex-1">
                            </input>
                        </div>
                        <div className="bg-gray-100 flex items-center w-64 p-2 mb-3">
                            <BiSolidLockAlt className="text-gray-400 m-2" />
                            <input type="password" name="password" placeholder="Passsword" className="bg-gray-100 outline-none text-sm flex-1">
                            </input>
                        </div>
                    </div>
                    <div className="flex px-24 mb-5 items-center justify-between align-items-center">
                        <label className="flex justify-center items-center text-xs"><input type="checkbox" name="remember" className="mr-1" /> Remember me </label>
                        <a href="#" className="text-xs">Forgot Password?</a>
                    </div>
                    <a href="/">
                        <button onClick={login} id="login-button" className="border-2 w-40 m-4 py-1 rounded-3xl text-lg font-semibold">Log In</button>
                    </a>
                </div>
                <div id="sidediv"
                    className="w-2/5 text-white rounded-tr-2xl rounded-br-2xl py-36 px-12">
                    <h2 className="text-3xl font-black">Don't have an account?</h2>
                    <a href="/">
                        <button onClick={goToSignUp} id="side-signup-button"
                            className="hover:bg-white border-white border-2 text-white w-40 m-4 py-1 rounded-3xl text-lg font-semibold">Sign Up</button>
                    </a>
                </div>
            </div>
        </main>
    )
}

export default LogIn;
