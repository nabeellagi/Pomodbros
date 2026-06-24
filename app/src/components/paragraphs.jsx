export default function P({ children, className, ...props }){
    return (
        <p
        className={`
        text-[20px] tracking-[1%]
        ${className}
        `}
        style={{
            fontFamily: "HiMelody"
        }}
        {...props}
        >
            {children}
        </p>
    )
}