import { createFileRoute } from '@tanstack/react-router';
import { motion } from 'framer-motion';

export const Route = createFileRoute('/')({
  component: TimerPage,
})

function TimerPage() {
  return <>
    <div className="relative w-full h-screen overflow-hidden">
      <motion.div
        className="relative"
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
      </motion.div>
    </div>
  </>
}


/**
Remaining Todos at this page
1. Set up fonts!!
2. 
*/