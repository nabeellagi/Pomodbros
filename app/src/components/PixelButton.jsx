import './style/PixelButton.css';

const type1 = 'buttons/button-pixel1.png'
const type2 = 'buttons/button-pixel2.png'
const type3 = 'buttons/button-pixel3.png'

const SPRITES = {
    1: type1,
    2: type2,
    3: type3
}

export function PixelButton({ children, className, pixelType = 1, onClick, width, height, ...props }){
    const sprite = SPRITES[pixelType] ?? SPRITES[1];

    return (
        <button
            className={`pixel-button ${className}`}
            style={{
                borderImageSource: `url(${sprite})`,
                width: width,
                height: height
            }}
            {...props}
            onClick={onClick}
        >
            <span className='pixel-button__label'>
                {children}
            </span>
        </button>
    )
}