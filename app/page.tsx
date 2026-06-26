import { getAllSkills } from '@/lib/skills'
import CatalogClient from '@/components/CatalogClient'

export default function HomePage() {
  const skills = getAllSkills()
  return <CatalogClient skills={skills} />
}
