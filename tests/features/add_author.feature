Feature: Add a new author
  Scenario: Add an author via the form
    Given I am on the homepage
    When I choose to add a new author
    And I fill out the author details
    And go back to homepage
    Then the new author should be added