import { render, screen } from '@testing-library/react';
import axios from 'axios';
import ProjectList from './ProjectList';

jest.mock('axios');

describe('ProjectList', () => {
  test('renders projects', async () => {
    const projects = {
      data: {
        projects: [
          { id: 1, name: 'Test Project', description: 'A test project', rating: 5 }
        ]
      }
    };
    axios.get.mockResolvedValue(projects);
    render(<ProjectList />);
    const projectElements = await screen.findAllByText(/Test Project/i);
    expect(projectElements.length).toBeGreaterThan(0); // Expect more than one match
  });
});