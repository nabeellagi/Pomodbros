import { useRef, useEffect, useState } from 'react'
import gsap from 'gsap'

const TAPES = [
    { id: 'casual', label: 'CASUAL', img: '/panels/tape1.png' },
    { id: 'completionist', label: 'COMPLETIONIST', img: '/panels/tape2.png' },
]

const STATES = {
    active: { top: 115, left: 0, scale: 0.5, opacity: 1, zIndex: 20 },
    inactive: { top: 90, left: -250, scale: 0.25, opacity: 0.8, zIndex: 10 },
}

const HOVER_BOOST = 1.15

export function TapeSelector({ defaultActive = 'casual', onChange }) {
    const [activeId, setActiveId] = useState(defaultActive)
    const [hoveredId, setHoveredId] = useState(null)
    const refs = useRef({})

    const setRef = (id) => (el) => {
        refs.current[id] = el
    }

    useEffect(() => {
        TAPES.forEach((tape) => {
            const el = refs.current[tape.id]
            if (!el) return

            const role = tape.id === activeId ? 'active' : 'inactive'
            const base = STATES[role]
            const isHovered = tape.id === hoveredId
            const scale = base.scale * (isHovered ? HOVER_BOOST : 1)

            gsap.killTweensOf(el)
            gsap.to(el, {
                top: base.top,
                left: base.left,
                scale,
                opacity: base.opacity,
                zIndex: base.zIndex,
                duration: 0.45,
                ease: 'back.out(1.6)',
                overwrite: 'auto',
            })
        })
    }, [activeId, hoveredId])

    const handleClick = (id) => {
        if (id === activeId) return
        setActiveId(id)
        onChange?.(id)
    }

    return (
        <div className="fixed inset-0 pointer-events-none [image-rendering:pixelated]">
            {TAPES.map((tape) => (
                <div
                    key={tape.id}
                    ref={setRef(tape.id)}
                    onClick={() => handleClick(tape.id)}
                    onMouseEnter={() => setHoveredId(tape.id)}
                    onMouseLeave={() => setHoveredId((current) => (current === tape.id ? null : current))}
                    className="absolute pointer-events-auto cursor-pointer rotate-[-11.3deg] origin-center"
                    style={{
                        top: STATES.inactive.top,
                        left: STATES.inactive.left,
                        zIndex: STATES.inactive.zIndex,
                        willChange: 'transform, opacity',
                    }}
                >
                    <img src={tape.img} alt={tape.label} draggable={false} />
                </div>
            ))}
        </div>
    )
}