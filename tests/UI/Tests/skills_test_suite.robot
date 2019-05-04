*** Settings ***
Library     SeleniumLibrary    
Resource    ../Settings/tests.txt

*** Test Cases ***
Open Website
    [Tags]    smoke 
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${BASE_URL}
    Wait Until Page Contains Element    ${profile_picture}    

Open Index Website
    [Tags]    smoke
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${URL_INDEX}
    Wait Until Page Contains Element    ${profile_picture}
    
Open Error Page Not Logged In
    [Tags]    smoke   
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${ERROR_URL}
    Check Error Page Elements
    Click Element    ${lnk_error_page}
    Check Elements Present Not Logged

Open Error Page Logged In
    [Tags]    smoke    logging    visitor
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${URL_INDEX}
    Log In With LinkedIn    LI_VISITOR_EMAIL    LI_VISITOR_PWD
    Go To    ${ERROR_URL}
    Check Error Page Elements
    Click Element    ${lnk_error_page}
    Check Elements Present Logged In Visitor

Elements Present Not Logged In
    [Tags]    smoke
    [Setup]    Open Website    ${BROWSER}    ${URL_INDEX}
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Check Elements Present Not Logged
    Go To    ${CAT_URL}
    Check Elements Present Not Logged
    
Log In With LinkedIn
    [Tags]    smoke    LinkdeIn    logging    visitor
    [Setup]    Open Website    ${BROWSER}    ${URL_INDEX}
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Log In With LinkedIn    LI_VISITOR_EMAIL    LI_VISITOR_PWD
    Check Elements Present Logged In Visitor
    
Log In And Log Out LinkedIn
    [Tags]    n-to-n    LinkedIn    logging    visitor
    [Setup]    Open Website    ${BROWSER}    ${URL_INDEX}
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Log In With LinkedIn    LI_VISITOR_EMAIL    LI_VISITOR_PWD
    Check Elements Present Logged In Visitor
    Log Out
    Check Elements Present Not Logged

Create LinkedIn Account
    [Tags]    n-to-n    LinkedIn    logging    visitor
    [Setup]    Run Keywords    Open Website    ${BROWSER}    ${URL_INDEX}    AND    Log In With LinkedIn    LI_VISITOR_EMAIL    LI_VISITOR_PWD    AND    Delete Account    AND    Close Browser
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser
    Open Website    ${BROWSER}    ${URL_INDEX}
    Log In With LinkedIn    LI_VISITOR_EMAIL    LI_VISITOR_PWD
    Check Elements Present Logged In Visitor

Delete Account
    [Tags]    n-to-n    LinkedIn    logging    visitor    deletion
    [Setup]    Open Website    ${BROWSER}    ${URL_INDEX}
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser    
    Log In With LinkedIn    LI_VISITOR_EMAIL    LI_VISITOR_PWD
    Delete Account
    Check Elements Present Not Logged

Go To Category And Back
    [Tags]    smoke    logging    admin    Facebook
    [Setup]    Open Website    ${BROWSER}    ${URL_INDEX}
    [Teardown]    Run Keywords    Capture Screenshot
    Log In With Facebook    FB_ADMIN_EMAIL    FB_ADMIN_PWD
    Go To Category
    Go Back From Category

Add Valid Categories
    [Tags]    validation    logging    admin    Facebook
    [Setup]    Run Keywords    Open Website    ${BROWSER}    ${URL_INDEX}    AND    Log In With Facebook    FB_ADMIN_EMAIL    FB_ADMIN_PWD
    [Teardown]    Run Keywords    Capture Screenshot    AND    Add All Skills    AND    Delete All Skills    AND    Close Browser 
    :FOR    ${cat}    IN    @{categories_valid}
    \    Go To Category
    \    Add Category    ${cat}

Add All Valid Categories, Skills, Delete All
    [Tags]    n-to-n    logging    admin    Facebook
    [Setup]    Run Keywords    Open Website    ${BROWSER}    ${URL_INDEX}    AND    Log In With Facebook    FB_ADMIN_EMAIL    FB_ADMIN_PWD
    [Teardown]    Run Keywords    Capture Screenshot    AND    Close Browser 
    Add All Categories
    Add All Skills
    Delete All Skills
    
    