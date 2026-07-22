import { Clock } from '@/components/clock'
import { PixelButton } from '@/components/PixelButton'
import Title from '@/components/title'
import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useState, useRef } from 'react'
import gsap from 'gsap'
import { H1 } from '@/components/headings'
import P from '@/components/paragraphs'
import { Counter } from '@/components/counter'
import { TapeSelector } from '@/components/TapeSelector'

export const Route = createFileRoute('/menu')({
  component: RouteComponent,
})

function RouteComponent() {
  const bg = useTimeOfDayBg();
  const clockRef = useRef(null);
  const wallRef = useRef(null);

  console.log("GSAP running", clockRef.current);

  useEffect(() => {
    // Clock animation
    gsap.fromTo(clockRef.current,
      {
        y: -100,
        opacity: 0,
      },
      {
        y: 0,
        opacity: 1,
        duration: 1.5,
        ease: "power3.out"
      }
    )

    // Wall animation
    gsap.fromTo(wallRef.current,
      {
        x: 200,
        opacity: 0
      },
      {
        x: 0,
        opacity: 1,
        duration: 4,
        ease: "power3.out"
      }
    )
  }, [])

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
        <div
          className="absolute right-6"
          ref={clockRef}
        >
          <Clock />
        </div>
      </div>
      <div
        className="fixed bottom-0 left-0 w-full"
        ref={wallRef}
      >
        <img
          src="/panels/wood.png"
          className="w-full"
        />
        <div className="absolute top-[168px] left-[128px] text-white">
          <H1 className="[text-shadow:2px_2px_0px_black]">How many sessions?</H1>
          <P className="[text-shadow:1px_1px_0px_black]">One Pomodoro consists of 25 minutes of focused work <br /> and a 5-minute break.</P>
        </div>
        <div className="absolute top-[90px] left-[600px]">
          <Counter />
        </div>
      </div>
      <div>
        <TapeSelector
          defaultActive="casual"
          onChange={(id) => console.log('Selected tape:', id)}
        />
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