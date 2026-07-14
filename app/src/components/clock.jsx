/**
CLOCK TIME
 */

import { useEffect, useState } from "react";

export function Clock(){
    const [time, setTime] = useState(() => getTime());

    useEffect(() => {
        const interval = setInterval(() => {
            setTime(getTime());
        }, 1000)
        return () => clearInterval(interval);
    }, []);

    return(
        <div>
            <img
                src="/panels/clock.png"
                className="w-full h-auto"
            />
            <h2
                className="absolute top-5/8 left-1/2 -translate-x-1/2 -translate-y-1/2
                text-[30px]
                [webkit-text-stroke:5px_#FFFFFF]"
                style={{
                    fontFamily: "Kavoon"
                }}
            >
                {time}
            </h2>
        </div>
    )
}

const getTime = () => {
    const now = new Date();
    return `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`
}