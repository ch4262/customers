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
    Then I should see "Customer REST API Service"
    And I should not see "404 Not Found"

