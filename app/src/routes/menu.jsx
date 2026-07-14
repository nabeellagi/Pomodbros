import { Clock } from '@/components/clock'
import { PixelButton } from '@/components/PixelButton'
import Title from '@/components/title'
import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useState } from 'react'

export const Route = createFileRoute('/menu')({
  component: RouteComponent,
})

function RouteComponent() {
  const bg = useTimeOfDayBg();
  return (
    <div
      className="flex flex-col items-center
      w-full h-screen [image-rendering:pixelated]"
      style={{
        backgroundImage: `url('${bg}')`,
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover'
      }}
    >
      <div className="relative w-full flex items-center justify-center">
        <Title>MENU</Title>
        <div className="absolute right-6">
          <Clock />
        </div>
      </div>
    </div>
  )
}

/**
 * Background will change based on time. 
 * There are exactly two variations! Day and sunset ig.
*/
const useTimeOfDayBg = () => {
  const getBg = () => {
    const hour = new Date().getHours();
    return hour <= 15 ? '/bg/day.png' : '/bg/sunset.png';
  }
  const [bg, setBg] = useState(getBg);

  useEffect(() => {
    const interval = setInterval(() => setBg(getBg()), 60000);
    return () => clearInterval(interval);
  }, [])

  return bg;
}

/**
TODO :
1. Bg change
2. Back btn
 */