import { BiSolidEnvelope, BiSolidLockAlt } from "react-icons/bi"
import { BsFillPersonFill } from "react-icons/bs"
import LogIn from "../Login/page";
const SignUp = () => {
    const goToLogIn = () => {
        // router.push('/Registration/SignUp');
        window.location.href = '/Registration/Login';
    };

    return (
        <main className="flex flex-col items-center justify-center min-h-screen">
            <div className="bg-white rounded-2xl shadow-md flex w-2/3 max-w-4xl text-center">
                <div className="w-3/5 py-5">
                    <div className="text-left font-black">
                        <p>CompanyName</p>
                    </div>
                    <div className="py-10">
                        <h2 id="text" className="font-extrabold text-3xl">Create Account</h2>
                    </div>
                    <div className="flex flex-col items-center px-">
                        <div className="bg-gray-100 w-64 p-2 flex items-center rounded-lg mb-3">
                            <BsFillPersonFill className="text-gray-400 m-2" />
                            <input type="text" placeholder="First Name" className="bg-gray-100 outline-none text-sm flex-1 " />
                        </div>
                        <div className="bg-gray-100 w-64 p-2 flex items-center rounded-lg mb-3">
                            <BsFillPersonFill className="text-gray-400 m-2" />
                            <input type="text" placeholder="Last Name" className="bg-gray-100 outline-none text-sm flex-1 " />
                        </div>
                        <div className="bg-gray-100 w-64 p-2 flex items-center rounded-lg mb-3">
                            <BiSolidEnvelope className="text-gray-400 m-2" />
                            <input type="email" placeholder="Email" className="bg-gray-100 outline-none text-sm flex-1 " />
                        </div>
                        <div className="bg-gray-100 w-64 p-2 flex items-center rounded-lg mb-3">
                            <BsFillPersonFill className="text-gray-400 m-2" />
                            <input type="text" placeholder="Username" className="bg-gray-100 outline-none text-sm flex-1 " />
                        </div>
                        <div className="bg-gray-100 w-64 p-2 flex items-center rounded-lg mb-3">
                            <BiSolidLockAlt className="text-gray-400 m-2" />
                            <input type="password" placeholder="Password" className="bg-gray-100 outline-none text-sm flex-1 " />
                        </div>
                        <div className="bg-gray-100 w-64 p-2 flex items-center rounded-lg mb-3">
                            <BiSolidLockAlt className="text-gray-400 m-2" />
                            <input type="password" placeholder="Confirm Password" className="bg-gray-100 outline-none text-sm flex-1 " />
                        </div>
                        <button id="signup-button" className="border-2 w-40 m-4 py-1 rounded-3xl text-lg font-semibold">Sign Up</button>
                    </div>
                </div>
                <div id="sidediv" className="w-2/5 text-white rounded-r-2xl py-40 px-12">
                    <h2 className="font-black text-3xl">Already have an account?</h2>
                    <button onClick={goToLogIn} id="side-login-button" className="hover:bg-white border-white border-2 text-white w-40 m-4 py-1 rounded-3xl text-lg font-semibold">Log In</button>
                </div>
            </div>
        </main>
    )
}

export default SignUp;