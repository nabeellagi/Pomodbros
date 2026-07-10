import { PixelButton } from '@/components/PixelButton'
import Title from '@/components/title'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/menu')({
  component: RouteComponent,
})

function RouteComponent() {
  return(
    <div className="flex flex-col items-center justify-center">
      <Title>
        MENU
      </Title>
      <div>
        
      </div>     
    </div>
  )
}
