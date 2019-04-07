*** Settings ***
Library     SeleniumLibrary    
Resource    ../Settings/tests.txt

*** Test Cases ***
Open Website
    [tags]    smoke
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${BASE_URL}
    Wait Until Page Contains Element    ${profile_picture}    

Open Index Website
    [tags]    smoke
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${URL_INDEX}
    Wait Until Page Contains Element    ${profile_picture}
    
Open Error Page Not Logged In
    [tags]    smoke
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Browser    ${ERROR_URL}    browser=${BROWSER}
    Maximize Browser Window
    Check Error Page Elements

Elements Present Not Logged In
    [tags]    smoke
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Browser    ${BASE_URL}    browser=${BROWSER}
    Maximize Browser Window
    Check Elements Present Not Logged
    Go To    ${CAT_URL}
    Check Elements Present Not Logged

Go To Category And Back
    [tags]    smoke
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${URL_INDEX}
    Go To Category
    Go Back From Category

Add Valid Categories
    [Tags]    validation
    [Setup]    Open Website    ${BROWSER}    ${URL_INDEX}    
    [Teardown]    Run Keywords    Capture Screenshot    AND    Add All Skills    AND    Delete All Skills    AND    Close Browser 
    :FOR    ${cat}    IN    @{categories_valid}
    \    Go To Category
    \    Add Category    ${cat}

Add All Valid Categories, Skills, Delete All
    [Tags]    n-to-n
    [Setup]    Open Website    ${BROWSER}    ${URL_INDEX}
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser 
    Add All Categories
    Add All Skills
    Delete All Skills
    
    