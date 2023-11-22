import { Button } from "@/components/ui/button";
import { 
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    SheetFooter,
    SheetClose
    } from "@/components/ui/sheet";
import { AlignJustify } from "lucide-react";
import Link from "next/link";


export default function Navbar() {
    return (
      <div id = "navbar" className="flex w-full h-full justify-between">
        <div className="flex mt-2">
          <Link href="/" className="mx-3">
              <h1 className="text-md">Home</h1>
          </Link>
          <Link href="/" className="mx-3">
              <h1 className="text-md">Report</h1>
          </Link>
        </div>
        <div>
          <div className="md:hidden">
              <Sheet>
                  <SheetTrigger>
                      <AlignJustify />
                  </SheetTrigger>
                  <SheetContent>
                      <SheetHeader>
                          <SheetDescription>
                              <div className="flex flex-col space-y-4 items-start w-full h-full text-lg mt-10">
                                  <Link
                                  href={"/"}>
                                      Profile
                                  </Link>
                                  <Link
                                  href={"/"}>
                                      Settings
                                  </Link>  
                                  <Link
                                  href={"/"}>
                                      Log Out
                                  </Link>                           
                              </div>
                          </SheetDescription>
                      </SheetHeader>
                  </SheetContent>
              </Sheet>
          </div>
          <div className="hidden md:flex md:space-x-4 text-white">
              <Button 
              className="text-md"
              id = "button"> 
                  Profile
              </Button>
              <Button 
              className="text-md"
              id = "button"> 
                  Settings
              </Button>
              <Button 
              className="text-md"
              id = "button">
                  Log Out
              </Button>  
          </div>
        </div>
    </div>
    )
};