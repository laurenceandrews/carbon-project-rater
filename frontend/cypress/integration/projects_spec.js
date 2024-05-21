describe('Projects Page', () => {
  it('successfully loads and displays projects', () => {
    // Arrange
    cy.visit('http://localhost:3000/')

    // Act - Nothing to do yet

    // Assert - Check that the main URL is loaded and projects are displayed
    cy.url().should('eq', 'http://localhost:3000/')
    cy.get('ul').find('li').should('have.length.at.least', 1)
  });
});
