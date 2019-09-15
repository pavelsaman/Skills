<?php
namespace Page\Acceptance;

class CategoryPage
{
	public static $profilePicture = '//img[contains(@class, "img-thumbnail")]';
    public static $categoryForm = '//form';
    public static $addCategory = '//button[@class="btn btn-info" and @name="new_category"]';
    public static $goBack = '//button[@class="btn btn-info" and @name="go_back"]';
    public static $greetingName = '//h4';
    public static $inputCategory = '//input[@name="category"]';
    public static $pleaseLogIn = '//div[@class="col-md-4 text-right"]/p';
    public static $error = '//div[@class="alert alert-info text-center"]';

    // text
    public static $pleaseLogInText = 'Please log in to go further.';
}
