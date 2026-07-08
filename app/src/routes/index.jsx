import { PixelButton } from '@/components/PixelButton';
import { createFileRoute } from '@tanstack/react-router';
import { motion } from 'framer-motion';

export const Route = createFileRoute('/')({
  component: TimerPage,
})

function TimerPage() {
  return <>
    <div className="relative w-full h-screen overflow-hidden">
      <motion.div
        className="absolute inset-0 [image-rendering:pixelated]"
        style={{
          backgroundImage: "url('bg/checker.png')",
          backgroundRepeat: "repeat",
          backgroundSize: "1350px 1350px"
        }}
        animate={{
          backgroundPosition: ["0px 0px", "1350px 1350px"]
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "backInOut"
        }}
      >
        <div
          className="flex flex-col items-center justify-center w-full h-[450px] bg-center bg-no-repeat bg-contain
            mt-[-30px]"
          style={{
            backgroundImage: "url('bg/tent.svg')"
          }}
        >
          <p
            className="font-[26px] text-white"
            style={{ fontFamily: "IndieFlower" }}
          >
            Start your activity with:
          </p>
          <img
            src="/logo.svg"
            width={300}
          />
        </div>
        <div className="flex justify-center items-center">
          <div className="grid grid-cols-2 gap-2 place-items-center w-[350px]">
            <PixelButton
              pixelType={3}
              className="color"
              width={150}
              height={50}
            >
              <span className="text-[#953240]">START!</span>
            </PixelButton>

            <div />

            <div />

            <PixelButton
              pixelType={3}
              className="color"
              width={150}
              height={50}
            >
              <span className="text-[#953240]">QUIT?</span>
            </PixelButton>
          </div>
        </div>
      </motion.div>
    </div>
  </>
}


/**
Remaining Todos at this page
1. Set up fonts!!
2. 
*/