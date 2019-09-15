<?php
namespace Page\Acceptance;

class LinkedIn
{
    public static $email = ['id' => 'username'];
    public static $password = ['id' => 'password'];
    public static $logIn = '//*[contains(@class, "btn__primary--large")]';
    public static $cancel = '//*[contains(@class, "btn__secondary--large")]';
}
