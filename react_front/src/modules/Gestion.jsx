import { useState, useEffect } from "react"



function Gestion() {
    const backend_url = "http://192.168.0.210:5000"
    const [isLoading, setIsLoading] = useState(true);
    const [perUsbData, setPerUsbData] = useState("{}")
    const [hubMap, setHubMap] = useState()
    useEffect(() => {
        fetch(backend_url + "/get_per_usb_data")
            .then((response) => response.json())
            .then((data) => {
                setPerUsbData(data)
                // setIsLoading(false);
            });
    }, []);

    useEffect(() => {
        fetch_usb_map()
    }, []);

    function fetch_usb_map() {

        fetch(backend_url + "/get_hubs")
            .then((response) => response.json())
            .then((data) => {
                setHubMap(data)
                setIsLoading(false);
                setTimeout(fetch_usb_map, 5000);
            });
    }




    if (isLoading) {
        return (<><div><h1>Cargando...</h1></div></>)
    }


    return (<>
        <div id="gestion">

            {hubMap.map((hub) => {
                return <div className="hub" key={hub}>
                    {hub.map((port) => {
                       return <p key={port} className="port">{port}</p>
                    })}

                </div>
            })}

        </div>

    </>);
}

export default Gestion;