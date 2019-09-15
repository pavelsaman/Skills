<?php
namespace Page\Acceptance;

class MainPage
{
    // page objects (elements)
    public static $profilePicture = '//img[contains(@class, "img-thumbnail")]';
    public static $facebookButton = ['id' => 'facebook'];
    public static $linkedInButton = ['id' => 'linkedin'];
    public static $logOutBtn = ['id' => 'logout'];
    public static $deleteBtn = ['id' => 'delete_account'];
    public static $logInElement = '//div[@class="col-md-4 text-right"]/p';
    public static $name = '//h1[@class="heading name"]';
    public static $skillsInfo = '//p[@class="paragraph"]';
    public static $skillsForm = '//form';
    public static $btnAdd = '//button[@class="btn btn-success"]';
    public static $addCategory = '//button[@class="btn btn-info"]';
    public static $greetingName = '//h4';
    public static $inputSkill = '//input[@name="skill"]';
    public static $selectCategory = '//select[@name="category"]';

    // static text
    public static $skillsTextInfo = 'Here you can find a list of my skills';
}
