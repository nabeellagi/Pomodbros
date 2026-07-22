import { createFileRoute } from '@tanstack/react-router'
import { Clock } from '@/components/clock'
import { PixelButton } from '@/components/PixelButton'
import Title from '@/components/title'
import { useEffect, useState, useRef } from 'react'
import gsap from 'gsap'
import { H1 } from '@/components/headings'
import P from '@/components/paragraphs'

export const Route = createFileRoute('/timer/casual')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/timer/casual"!</div>
}
