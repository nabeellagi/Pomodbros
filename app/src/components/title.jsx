
export default function Title({ children, className, ...props }) {
  return (
    <h1
      className={`
      text-[50px] text-center tracking-[15%] uppercase
      ${className}
      `}
      style={{
        fontFamily: 'CherryBombOne'
      }}
      {...props}
    >
      {children}
    </h1>
  );
}