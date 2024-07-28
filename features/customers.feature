Feature: The pet store service back-end
    As a Pet Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my pets

Background:
    Given the following customers
      | name       | address                  | email                 | phone_number  | member_since | status   |
      | Fluffy     | 123 Pet Lane, Dogtown    | fluffy@example.com    | 555-1234      | 2021-05-12   | active   |
      | Whiskers   | 456 Cat St, Meow City    | whiskers@example.com  | 555-5678      | 2020-11-23   | suspended|
      | Rex        | 789 Woof Blvd, Barkburg  | rex@example.com       | 555-9876      | 2019-07-01   | active   |
      | Tweety     | 321 Bird Ave, Aviary     | tweety@example.com    | 555-6543      | 2022-02-18   | active   |


Scenario: The server is running
    When I visit the "home page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "Name" to "Sai"
    And I set the "Address" to "80 Court House"
    And I set the "Email" to "sb@nyu.edu"
    And I set the "Phone" to "5512298011"
    And I select "Active" in the "Status" dropdown
    And I set the "Since" to "06-16-2022"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Address" field should be empty
    And the "Email" field should be empty
    And the "Phone" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Sai" in the "Name" field
    And I should see "80 Court House" in the "Address" field
    And I should see "sb@nyu.edu" in the "Email" field
    And I should see "5512298011" in the "Phone" field
    And I should see "2022-06-16" in the "Since" field
    And I should see "Active" in the "Status" dropdown

