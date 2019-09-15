<?php 

use Step\Acceptance\Keywords as KeywordTester;
use Resources\Resources as res;

class LogInCest
{
    // before each test
    public function _before(AcceptanceTester $I)
    {

    }

    public function _after(AcceptanceTester $I)
    {
        
    }

    // after each passed test
    public function _passed(\AcceptanceTester $I)
    {
        //$I->wait(300);
    }

    public function _failed(\AcceptanceTester $I)
    {
        //$I->wait(300);
    }

    /**
     * @group linkedin
     * @group login
    */
    public function logInWithLinkedIn(KeywordTester $I)
    {
    	$I->logInLinkedIn(res::$user, res::$validEmail, res::$validPasswordLI);    
        $I->seeMainPageAsVisitor(res::$user);  
    }    
    
    /**
     * @group linkedin
     * @group login
     * @group category
    */
    public function logInWithLinkedInGoToCategory(KeywordTester $I)
    {
        $I->logInLinkedIn(res::$user, res::$validEmail, res::$validPasswordLI);    
        $I->seeMainPageAsVisitor(res::$user);  
        $I->categoryPageLoggedInVisitorShouldContain(res::$user);
    }

    /**
     * @group linkedin
     * @group login
     * @group logout
     * @group category
    */
    public function logInWithLinkedInAndLogOutFromMainPage(KeywordTester $I)
    {
        $I->logInLinkedIn(res::$user, res::$validEmail, res::$validPasswordLI);    
        $I->seeMainPageAsVisitor(res::$user);  
        $I->logOutFromMainPage();
    }

    /**
     * @group linkedin
     * @group login
     * @group logout
     * @group category
    */
    public function logInWithLinkedInAndLogOutFromCategoryPage(KeywordTester $I)
    {
        $I->logInLinkedIn(res::$user, res::$validEmail, res::$validPasswordLI);    
        $I->seeMainPageAsVisitor(res::$user);  
        $I->logOutFromCategoryPage();
    }    
}
