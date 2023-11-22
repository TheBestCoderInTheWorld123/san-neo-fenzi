
import {BiSolidEnvelope, BiSolidLockAlt} from "react-icons/bi"
const LogIn = () => {
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
                            <BiSolidEnvelope className="text-gray-400 m-2" />
                            <input type="email" name="email" placeholder="Email" className="bg-gray-100 outline-none text-sm flex-1">
                            </input>
                        </div>
                        <div className="bg-gray-100 flex items-center w-64 p-2 mb-3">
                            <BiSolidLockAlt className="text-gray-400 m-2" />
                            <input type="password" name="password" placeholder="Passsword" className="bg-gray-100 outline-none text-sm flex-1">
                            </input>
                        </div>
                    </div>
                    <div className="flex px-24 mb-5 items-center justify-between align-items-center">
                     <label className="flex justify-center items-center text-xs"><input type="checkbox" name="remember" className="mr-1"/> Remember me </label>
                        <a href="#" className="text-xs">Forgot Password?</a>
                    </div>
                    <a href="/">
                        <button id="login-button" className= "border-2 w-40 m-4 py-1 rounded-3xl text-lg font-semibold">Log In</button>
                    </a>
            </div>
            <div id="sidediv"
            className="w-2/5 text-white rounded-tr-2xl rounded-br-2xl py-36 px-12">
                <h2 className="text-3xl font-black">Don't have an account?</h2>
                <a href="/">
                    <button id="side-signup-button"
                    className= "hover:bg-white border-white border-2 text-white w-40 m-4 py-1 rounded-3xl text-lg font-semibold">Sign Up</button>
                </a>
            </div>
        </div>
        </main>
    )
  }

  export default LogIn;
