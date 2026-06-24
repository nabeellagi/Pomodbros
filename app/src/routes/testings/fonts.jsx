import { createFileRoute } from '@tanstack/react-router'
import Title from '@/components/title'
import { H1, H2 } from '@/components/headings'
import P from '@/components/paragraphs'


export const Route = createFileRoute('/testings/fonts')({
  component: RouteComponent,
})

function RouteComponent() {
  return <>
    <div>
      <Title>TITLE</Title> 
      <H1>Heading 1</H1>
      <H2>Heading 2</H2>
      <P>This is the text dude, now it is <b>BOLD</b> and so <i>ITALIC</i> comes.</P>
    </div>
  </>
}
