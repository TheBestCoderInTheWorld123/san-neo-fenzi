"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { BiSolidLockAlt } from "react-icons/bi";
import { IoMdPerson } from "react-icons/io";

const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const login = async () => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "username": username,
                "password": password
            })
        };

        try {
            const response = await fetch('http://51.20.249.252:8000/login', requestOptions);
            const data = await response.json();
            // console.log(data);

            if (data['status_code'] === 101) {
                router.push("/Home");
            }
        } catch (error) {
            console.error('Error:', error);
        }
        finally {
            setIsLoading(false); // Stop loading regardless of the outcome
        }
    };

    const goToSignUp = () => {
        router.push('/Registration/SignUp');
    };

    return (
        <main className="flex flex-col items-center justify-center min-h-screen px-4">
        <div className="bg-white rounded-2xl shadow-md w-full max-w-lg sm:max-w-xl md:max-w-2xl lg:max-w-4xl mx-auto text-center">
            <div className="flex flex-col md:flex-row">
                <div className="w-full md:w-3/5 p-5">
                    <div className="text-left px-4 font-black">
                        <p className="text-sm sm:text-base md:text-lg">Penguin CRM Private Limited</p>
                    </div>
                    <div className="py-10">
                        <h2 className="font-extrabold text-xl sm:text-2xl md:text-3xl">Login To Your Account</h2>
                    </div>
                    <div className="flex flex-col items-center">
                        <div className="bg-gray-100 flex items-center w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg p-2 mb-3">
                            <IoMdPerson className="text-gray-400 m-2" />
                            <input 
                                value={username} 
                                onChange={handleUsernameChange} 
                                type="text" 
                                name="username" 
                                placeholder="Username" 
                                className="bg-gray-100 outline-none text-sm flex-1"
                            />
                        </div>
                        <div className="bg-gray-100 flex items-center w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg p-2 mb-3">
                            <BiSolidLockAlt className="text-gray-400 m-2" />
                            <input 
                                value={password} 
                                onChange={handlePasswordChange} 
                                type="password" 
                                name="password" 
                                placeholder="Password" 
                                className="bg-gray-100 outline-none text-sm flex-1"
                            />
                        </div>
                    </div>
                    <div className="flex px-8 sm:px-16 md:px-24 mb-5 items-center justify-between">
                        <label className="flex justify-center items-center text-xs sm:text-sm"><input type="checkbox" name="remember" className="mr-1" /> Remember me </label>
                        <a href="#" className="text-xs sm:text-sm">Forgot Password?</a>
                    </div>
                    <button 
                        onClick={login} 
                        id="login-button" 
                        className="border-2 w-40 m-4 py-1 rounded-3xl text-lg font-semibold" 
                        disabled={isLoading}
                    >
                        {isLoading ? 'Processing...' : 'Log In'}
                    </button>
                </div>
                <div id='login-side-div' className="hidden md:block md:w-2/5 text-white rounded-br-2xl py-36 px-12">
                    <h2 className="text-2xl sm:text-3xl font-black">Don&apos;t have an account?</h2>
                    <button onClick={goToSignUp} id='side-login-button' className="hover:bg-white hover:text-2f455c border-white border-2 text-white w-40 m-4 py-1 rounded-3xl text-lg font-semibold">Sign Up</button>
                </div>
            </div>
        </div>
    </main>    );
};

export default LogIn;
