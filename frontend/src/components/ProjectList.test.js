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
    const projectElement = await screen.findByText(/Test Project/i);
    expect(projectElement).toBeInTheDocument();
  });
});