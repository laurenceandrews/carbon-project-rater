describe('Projects Page', () => {
    it('successfully loads and displays projects', () => {
      // Arrange
      cy.visit('http://localhost:3000/')
  
      // Act
      cy.contains('Projects').click();
  
      // Assert
      cy.url().should('include', '/projects')
      cy.get('ul').find('li').should('have.length.at.least', 1)
    });
  });
  