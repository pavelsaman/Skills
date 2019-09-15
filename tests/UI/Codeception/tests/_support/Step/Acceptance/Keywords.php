<?php
namespace Step\Acceptance;

// hide sensitive data
use \Codeception\Step\Argument\PasswordArgument;
use Page\Acceptance\MainPage as MP;
use Page\Acceptance\CategoryPage as CP;
use Page\Acceptance\Facebook as FB;
use Page\Acceptance\LinkedIn as LI;
use Page\Acceptance\ErrorPage as ER;
use Resources\Resources as res;

class Keywords extends \AcceptanceTester
{

	public function amOnMainPage()
	{
		$I = $this;
		$I->amOnPage(res::$urlMain);	
		$I->mainPageLoggedOutShouldContain();	
	}	

	public function amOnCategoryPage()
	{
		$I = $this;
		$I->amOnPage(res::$urlCategory);
	}

	public function amOnErrorPage($link)
	{
		$I = $this;
		$I->amOnPage($link);
	}

	public function goToCategoryPage()
	{
		$I = $this;
		$I->click(MP::$addCategory);
		$I->seeCategoryTable();
	}

	public function goToCategoryPageViaLink()
	{
		$I = $this;
		$I->amOnPage(res::$urlCategory);		
	}

	public function goToSkillPage()
	{
		$I = $this;
		$I->click(CP::$goBack);
		$I->seeSkillsTable();
	}

	public function seeSkillsTable()
	{
		$I = $this;
		$I->waitForElementVisible(MP::$skillsForm);
		$I->seeElement(MP::$inputSkill);
		$I->seeElement(MP::$selectCategory);
		$I->seeElement(MP::$btnAdd);
		$I->seeElement(MP::$addCategory);
	}	

	public function dontSeeSkillsTable()
	{
		$I = $this;
		$I->waitForElementVisible(MP::$profilePicture);
		$I->dontSeeElement(MP::$inputSkill);
		$I->dontSeeElement(MP::$selectCategory);
		$I->dontSeeElement(MP::$btnAdd);
		$I->dontSeeElement(MP::$addCategory);
	}

	public function seeCategoryTable()
	{
		$I = $this;
		$I->waitForElementVisible(CP::$categoryForm);
		$I->seeElement(CP::$inputCategory);
		$I->seeElement(CP::$addCategory);
		$I->seeElement(CP::$goBack);
	}	

	public function dontSeeCategoryTable()
	{
		$I = $this;
		$I->waitForElementVisible(CP::$profilePicture);
		$I->dontSeeElement(CP::$inputCategory);
		$I->dontSeeElement(CP::$addCategory);
		$I->dontSeeElement(CP::$goBack);
	}

	public function seeTesterName($desiredName)
	{
		$I = $this;
		$I->waitForElementVisible(MP::$name);
		$pageName = $I->grabTextFrom(MP::$name);
		$I->assertEquals($pageName, $desiredName);
	}	

	public function seeInSkillsText()
	{
		$I = $this;
		$skillsTextPage = $I->grabTextFrom(MP::$skillsInfo);
		$I->assertEquals($skillsTextPage, MP::$skillsTextInfo);
	}

	public function seeNameInGreeting($name)
	{
		$I = $this;
		$greeting= $I->grabTextFrom(MP::$greetingName);
		$I->assertNotEquals($I->seeInString($greeting, $name), false);
	}			

	public function seePleaseLogInText()
	{
		$I = $this;
		$I->waitForElementVisible(CP::$pleaseLogIn);
		$text= $I->grabTextFrom(CP::$pleaseLogIn);
		$I->assertEquals($text, CP::$pleaseLogInText);
	}

	public function seeTextInMainError()
	{
		$I = $this;
		$I->waitForElementVisible(ER::$mainError);
		$error = $I->grabTextFrom(ER::$mainError);
		$I->assertEquals($error, ER::$mainErrorText);
	}

	public function seeTextInSmallError()
	{
		$I = $this;
		$I->waitForElementVisible(ER::$smallError);
		$error = $I->grabTextFrom(ER::$smallError);
		$I->assertEquals($error, ER::$smallErrorText);
	}

	public function seeLinkOnErrorPage()
	{
		$I = $this;
		$I->waitForElementVisible(ER::$smallError);
		$I->seeLink(ER::$linkText, res::$urlMain);
	}

	public function mainPageLoggedInAdminShouldContain($username)
	{
		$I = $this;
		$I->waitForElementVisible(MP::$profilePicture);
		$I->waitForElementVisible(MP::$name);
		$I->waitForElementVisible(MP::$logOutBtn);
		$I->waitForElementVisible(MP::$deleteBtn);
		$I->seeInSkillsText();
		$I->seeNameInGreeting($username);
		$I->seeSkillsTable();
	}	

	public function mainPageLoggedInVisitorShouldContain($username)
	{
		$I = $this;
		$I->waitForElementVisible(MP::$profilePicture);
		$I->waitForElementVisible(MP::$name);
		$I->waitForElementVisible(MP::$logOutBtn);
		$I->waitForElementVisible(MP::$deleteBtn);
		$I->seeInSkillsText();
		$I->seeNameInGreeting($username);
		$I->dontSeeSkillsTable();
	}	

	public function mainPageLoggedOutShouldContain()
	{
		$I = $this;
		$I->waitForElementVisible(MP::$profilePicture);
		$I->waitForElementVisible(MP::$facebookButton);
		$I->waitForElementVisible(MP::$linkedInButton);
		$I->waitForElementVisible(MP::$name);
		$I->seeInSkillsText();
		$I->dontSeeSkillsTable();
	}

	public function categoryPageLoggedOutShouldContain()
	{
		$I = $this;
		$I->waitForElementVisible(MP::$profilePicture);
		$I->waitForElementVisible(MP::$facebookButton);
		$I->waitForElementVisible(MP::$linkedInButton);
		$I->waitForElementVisible(MP::$name);
		$I->seeInSkillsText();
		$I->dontSeeCategoryTable();
	}

	public function categoryPageLoggedInVisitorShouldContain($username)
	{
		$I = $this;
		$I->waitForElementVisible(MP::$profilePicture);
		$I->waitForElementVisible(MP::$name);
		$I->waitForElementVisible(MP::$logOutBtn);
		$I->waitForElementVisible(MP::$deleteBtn);
		$I->seeInSkillsText();
		$I->seeNameInGreeting($username);
		$I->dontSeeCategoryTable();
	}	

	public function logIn($userField, $pwdField, $logInBtn, $username, $email, $password)
	{
		$I = $this;
		$I->waitForElementVisible($userField);
		$I->fillField($userField, $email);
		$I->fillField($pwdField, new PasswordArgument($password));
		$I->click($logInBtn);				
	}

	public function logInLinkedIn($username, $email, $password)
	{
		$I = $this;
		$I->amOnMainPage();
		$I->click(MP::$linkedInButton);
		$I->logIn(LI::$email, LI::$password, LI::$logIn, $username, $email, $password);					
	}	

	public function logInFacebook($username, $email, $password)
	{
		$I = $this;
		$I->amOnMainPage();
		$I->click(MP::$facebookButton);
		$I->logIn(FB::$email, FB::$password, FB::$logIn, $username, $email, $password);		
	}

	public function seeMainPageAsVisitor($username)
	{
		$I = $this;				
		$I->mainPageLoggedInVisitorShouldContain($username);			
	}

	public function seeMainPageAsAdmin($username)
	{
		$I = $this;
		$I->mainPageLoggedInAdminShouldContain($username);		
	}

	public function logOutFromMainPage()
	{
		$I = $this;
		$I->waitForElementVisible(MP::$logOutBtn);
		$I->click(MP::$logOutBtn);
		$I->mainPageLoggedOutShouldContain();		
	}

	public function logOutFromCategoryPage()
	{
		$I = $this;
		$I->waitForElementVisible(MP::$logOutBtn);
		$I->click(MP::$logOutBtn);
		$I->categoryPageLoggedOutShouldContain();		
	}

	public function addCategory($category)
	{
		$I = $this;
		$I->fillField(CP::$inputCategory, $category);
		$I->click(CP::$addCategory);		
	}

	public function seeCategoryError($errorText)
	{
		$I = $this;
		$I->waitForElementVisible(CP::$error);
		$error = $I->grabTextFrom(CP::$error);
		$I->assertEquals($error, $errorText);
	}
}