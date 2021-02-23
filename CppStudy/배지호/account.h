#pragma once
#include <iostream>
#include <cstring>

using namespace std;

class Account         //계좌 클래스
{
public:
	Account(int id, char name[], int money);
	~Account();

	int compare_id(int id);     // id와 계좌 아이디 비교 

	void add_money(int money);   // money 증가
	void sub_money(int money);   // money 감소
	void show_cus() const;        // 계좌 클래스

private:

	int my_id;							
	char *my_name = new char[20];    
	int my_money;

};


