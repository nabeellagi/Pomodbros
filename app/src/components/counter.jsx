import { useRef, useState } from 'react';
import gsap from 'gsap';

const MIN = 1
const MAX = 9

export function Counter({ className = '' }) {
    const [count, setCount] = useState(1);
    const numberRef = useRef(null);
    const upRef = useRef(null);
    const downRef = useRef(null);

    const popNumber = () => {
        const el = numberRef.current;
        if (!el) return
        gsap.killTweensOf(el)
        gsap.fromTo(el,
            {
                scale: 1,
            },
            {
                scale: 1.35,
                duration: 0.12,
                ease: "power2.out",
                yoyo: true,
                repeat: 1,
                overwrite: 'auto'
            }
        )
    }

    const pressButton = (ref) => {
        const el = ref.current;
        if (!el) return
        gsap.killTweensOf(el)
        gsap.fromTo(
            el,
            { scale: 1 },
            {
                scale: 0.82,
                duration: 0.08,
                ease: 'power1.out',
                yoyo: true,
                repeat: 1,
                overwrite: 'auto',
            }
        )
    }

    const increment = () => {
        setCount((c) => (c >= MAX ? MIN : c + 1))
        popNumber()
        pressButton(upRef)
    }

    const decrement = () => {
        setCount((c) => (c <= MIN ? MAX : c - 1))
        popNumber()
        pressButton(downRef)
    }


    return (
        <div
            className={`relative flex flex-col items-center justify-between
      w-[65px] h-[196px] rounded-full bg-[#F5920A]
      border-[3px] border-black [image-rendering:pixelated] py-3 ${className}`}
        >
            <button
                ref={upRef}
                onClick={increment}
                aria-label="Increase count"
                className="focus:outline-none cursor-pointer"
            >
                <svg width="32" height="28" viewBox="0 0 32 28">
                    <polygon
                        points="16,0 32,28 0,28"
                        fill="#6B4226"
                        stroke="black"
                        strokeWidth="3"
                        strokeLinejoin="round"
                    />
                </svg>
            </button>

            <span
                ref={numberRef}
                className="text-black font-black text-6xl leading-none select-none"
                style={{
                    fontFamily: "Kavoon"
                }}
            >
                {count}
            </span>

            <button
                ref={downRef}
                onClick={decrement}
                aria-label="Decrease count"
                className="focus:outline-none cursor-pointer"
            >
                <svg width="32" height="28" viewBox="0 0 32 28">
                    <polygon
                        points="0,0 32,0 16,28"
                        fill="#6B4226"
                        stroke="black"
                        strokeWidth="3"
                        strokeLinejoin="round"
                    />
                </svg>
            </button>
        </div>
    )
}