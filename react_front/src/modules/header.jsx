import { Link } from "react-router-dom";


function Header() {
    return (
        <>
            <div id="header">
                <Link to="/">
                    <button>Volver</button>
                </Link>
            </div>
        </>
    );
}

export default Header;