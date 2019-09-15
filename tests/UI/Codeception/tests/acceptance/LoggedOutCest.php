<?php 

use Step\Acceptance\Keywords as KeywordTester;

class LoggedOutCest
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
    * @group smoke
    * @group main_page
    */
    public function mainPageNotLoggedIn(KeywordTester $I)
    {    	
    	$I->amOnMainPage();
    }

    /**
    * @group smoke
    * @group category
    */
    public function categoryPageNotLoggedIn(KeywordTester $I)
    {       
        $I->amOnCategoryPage();        
        $I->seePleaseLogInText();
        $I->seeInCurrentUrl('category');
        $I->categoryPageLoggedOutShouldContain();
    }

    /**
    * @group smoke
    * @group main_page
    */
    public function mainPageTesterNameShouldBe(KeywordTester $I)
    {    	
    	$I->amOnMainPage();
    	$I->seeTesterName('Pavel Šaman');
    }

    /**
    * @group smoke
    * @group error_page
    */
    public function errorPageContains(KeywordTester $I)
    {       
        $I->amOnErrorPage('/blabal');
        $I->seeTextInMainError();
        $I->seeTextInSmallError();
        $I->seeLinkOnErrorPage();
    }        
}
