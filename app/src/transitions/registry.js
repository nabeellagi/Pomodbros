export const transitions = {
    circleWipe: {
        getKeyframes: (origin) => ({
            initial: { clipPath: `circle(0% at ${origin.x}px ${origin.y}px)` },
            covered: { clipPath: `circle(150% at ${origin.x}px ${origin.y}px)` },
            revealed: { clipPath: `circle(0% at ${origin.x}px ${origin.y}px)` },
        }),
        duration: 0.5,
        ease: [0.76, 0, 0.24, 1],
    },
    slideUp: {
        getKeyframes: () => ({
            initial: { y: '100%' },
            covered: { y: '0%' },
            revealed: { y: '-100%' },
        }),
        duration: 0.4,
        ease: 'easeInOut',
    },
};