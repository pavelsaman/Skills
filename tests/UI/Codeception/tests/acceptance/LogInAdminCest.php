<?php 

use Step\Acceptance\Keywords as KeywordTester;
use Resources\Resources as res;

class LogInAdminCest
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

    // tests

    /**
     * @group facebook
     * @group login
    */
    public function logInWithFacebook(KeywordTester $I)
    {
    	$I->logInFacebook(res::$user, res::$validEmail, res::$validPasswordFB);
    	$I->seeMainPageAsAdmin(res::$user);
    }

    /**
     * @group facebook
     * @group login
     * @group logout
    */
    public function logInWithFacebookAndLogOutFromMainPage(KeywordTester $I)
    {
    	$I->logInFacebook(res::$user, res::$validEmail, res::$validPasswordFB);
    	$I->seeMainPageAsAdmin(res::$user);
    	$I->logOutFromMainPage();
    }

    /**
     * @group facebook
     * @group login
     * @group category
    */
    public function logInWithFacebookAndGoToCategoryPageViaLink(KeywordTester $I)
    {
    	$I->logInFacebook(res::$user, res::$validEmail, res::$validPasswordFB);
    	$I->seeMainPageAsAdmin(res::$user);
    	$I->amOnCategoryPage();
    	$I->seeCategoryTable();
    }

    /**
     * @group facebook
     * @group login
     * @group category
    */
    public function logInWithFacebookAndGoToCategoryPage(KeywordTester $I)
    {
    	$I->logInFacebook(res::$user, res::$validEmail, res::$validPasswordFB);
    	$I->seeMainPageAsAdmin(res::$user);
    	$I->goToCategoryPage();    	
    }

    /**
     * @group facebook
     * @group login
     * @group category
     * @example { "category_name": "test" }
     * @example { "category_name": "testing" }
     * @example { "category_name": "flask" }
    */
    public function createNewCategory(KeywordTester $I, \Codeception\Example $example)
    {
    	$I->logInFacebook(res::$user, res::$validEmail, res::$validPasswordFB);
    	$I->seeMainPageAsAdmin(res::$user);
    	$I->goToCategoryPage();    	
    	$I->addCategory($example['category_name']);    	
    	$I->seeMainPageAsAdmin(res::$user);
    }

    /**
     * @group facebook
     * @group login
     * @group category
     * @example { "category_name": "1", "error": "The length has to be at least 2 characters, maximum 30 characters." }
     * @example { "category_name": "test@@@", "error": "The field contains invalid characters." }
     * @example { "category_name": "", "error": "Category field is required." }
    */
    public function createNewCategoryError(KeywordTester $I, \Codeception\Example $example)
    {
    	$I->logInFacebook(res::$user, res::$validEmail, res::$validPasswordFB);
    	$I->seeMainPageAsAdmin(res::$user);
    	$I->goToCategoryPage();    	
    	$I->addCategory($example['category_name']);    	
    	$I->seeCategoryTable();
    	$I->seeCategoryError($example['error']);
    }

    /**
     * @group facebook
     * @group login
     * @group category
     * @group duplicate
     * @example { "category_name": "test", "error": "Entered category is not unique." }
    */
    public function createNewCategoryErrorDuplicate(KeywordTester $I, \Codeception\Example $example)
    {
    	$I->logInFacebook(res::$user, res::$validEmail, res::$validPasswordFB);
    	$I->seeMainPageAsAdmin(res::$user);
    	$I->goToCategoryPage();    	
    	$I->addCategory($example['category_name']);  
    	$I->seeMainPageAsAdmin(res::$user);  	
    	$I->goToCategoryPage(); 
    	$I->addCategory($example['category_name']); 
    	$I->seeCategoryTable();
    	$I->seeCategoryError($example['error']);
    }
}
