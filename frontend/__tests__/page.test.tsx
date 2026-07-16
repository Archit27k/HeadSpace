import { render, screen } from '@testing-library/react'
import LandingPage from '../src/app/page'

describe('LandingPage', () => {
  it('renders a heading', () => {
    render(<LandingPage />)

    const heading = screen.getByRole('heading', {
      name: /Your Personal AI/i,
    })

    expect(heading).toBeInTheDocument()
  })
})
