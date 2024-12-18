describe('Sample Test', () => {
    it('Sample Test to visit home page', () => {
        cy.wait(500);
        cy.visit('/');
        cy.wait(500);
        cy.contains('Sign in');
        cy.contains('Sign up');
        cy.contains('About');
        cy.contains('Team');
    });
});
