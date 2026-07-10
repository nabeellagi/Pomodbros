import { createContext, useContext, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from '@tanstack/react-router';
import { transitions } from './registry';

const TransitionContext = createContext(null);

export function TransitionProvider({ children }) {
  const navigate = useNavigate();
  const [phase, setPhase] = useState(null); // null | 'covering' | 'revealing'
  const [config, setConfig] = useState(null);

  const goTo = useCallback((to, { type = 'circleWipe', origin } = {}) => {
    const def = transitions[type];
    const originPoint = origin ?? { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    const keyframes = def.getKeyframes(originPoint); // computed once, not per render
    setConfig({ def, keyframes, to });
    setPhase('covering');
  }, []);

  const handleCoverComplete = () => {
    navigate({ to: config.to });
    setPhase('revealing');
  };

  const handleRevealComplete = () => {
    setPhase(null);
    setConfig(null);
  };

  return (
    <TransitionContext.Provider value={{ goTo }}>
      {children}
      <AnimatePresence>
        {phase && config && (
          <motion.div
            className="fixed inset-0 z-[999] pointer-events-none bg-black"
            initial={config.keyframes.initial}
            animate={phase === 'covering' ? config.keyframes.covered : config.keyframes.revealed}
            transition={{ duration: config.def.duration, ease: config.def.ease }}
            onAnimationComplete={
              phase === 'covering' ? handleCoverComplete : handleRevealComplete
            }
          />
        )}
      </AnimatePresence>
    </TransitionContext.Provider>
  );
}

export function usePageTransition() {
  const ctx = useContext(TransitionContext);
  if (!ctx) throw new Error('usePageTransition must be used inside TransitionProvider');
  return ctx;
}