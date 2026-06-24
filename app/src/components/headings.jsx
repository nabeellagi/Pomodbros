export function H1({ children, className, ...props }) {
  return (
    <h1
      className={`
      text-[30px] tracking-[1%]
      ${className}
      `}
      style={{
        fontFamily: "Kavoon"
      }}
      {...props}
    >
      {children}
    </h1>
  );
}

export function H2({ children, className, ...props }) {
  return (
    <h2
      className={`
      text-[25px] tracking-[5%]
      ${className}
      `}
      style={{
        fontFamily: "Kavoon"
      }}
    >
      {children}
    </h2>
  )
}