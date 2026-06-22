---
name: run-tests
description: Run Maven tests for Selenium or REST Assured project with correct directory and suite flags. Accepts optional suite name argument (e.g. /run-tests smoke).
disable-model-invocation: true
---

Run Maven tests for the correct AI3x Java project.

Projects:
- **Selenium Framework**: `chapter_02_Prompt_Eng/Project2_Selenium_Framework/AdvanceSeleniumFramework/`
  - Full suite: `mvn clean test`
  - Specific suite: `mvn test -DsuiteXmlFile=testng-$ARGUMENTS.xml`
- **REST API Framework**: `Project_02_REST_API_Framework/RICEPOT_RESTASSURED_API_Project/`
  - Full suite: `mvn test` (Allure report artifacts generated in target/)

Steps:
1. Identify which project from context or ask
2. If $ARGUMENTS provided, treat as suite name → append `-DsuiteXmlFile=testng-$ARGUMENTS.xml`
3. Run from the correct sub-directory (cd first)
4. Report pass/fail count and Allure report path if generated
