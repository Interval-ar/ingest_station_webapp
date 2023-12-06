import { Link } from "react-router-dom";

function Main_page() {
    return (<>
        <div id="main">
            <div>
                <h1>Interval - Ingest station</h1>
            </div>
            <div>
                <Link to="gestion">
                    <button>Gestion</button>
                </Link>
                <Link to="config">
                    <button>Configurar</button>
                </Link>
            </div>

        </div>
    </>);
}

export default Main_page;