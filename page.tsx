import TablePage from "./table";
import Navbar from "./navbar"

export default function Report() {
    return (
        <main>
            {/* main div */}
            <div>
                <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
                    <Navbar />
                </div>
                {/* main page div */}
                <div>
                    {/* map & piechart */}
                    <div>
                        {/* map div */}
                        <div></div>
                        {/* piechart div */}
                        <div></div>
                    </div>
                    {/* table div */}
                    <div>
                        <TablePage />
                    </div>
                </div>
                {/*bottom bar */}
                <div></div>
            </div>
        </main>
    )
};