import LogIn from "./Registration/Login/page";
import dynamic from "next/dynamic";
import SignUp from "./Registration/SignUp/page";
import Report from "./Report/page";

export default function Home() {
  const LogIn = dynamic(() => import('./Registration/Login/page'), { ssr: false });
  const SignUp = dynamic(() => import('./Registration/SignUp/page'), { ssr: false });
  const Report = dynamic(() => import('./Report/page'), { ssr: false });
  return (
    <div>
      <LogIn/>
    </div>
  )
}
