#include "account.h"


Account::Account(int id, char name[], int money) :my_id(id), my_money(money)
{
	strcpy(my_name, name);
}

Account::~Account()
{
	delete[] my_name;
}

int Account::compare_id(int id)
{
	if (id == my_id)
		return 1;
	else
		return 0;
}

void Account::add_money(int money)
{
	my_money += money;
}

void Account::sub_money(int money)
{
	my_money -= money;
}

void Account::show_cus() const
{
	cout << "------------------------" << endl;
	cout << "°èÁÂID: " << my_id << endl;
	cout << "ÀÌ¸§: " << my_name << endl;
	cout << "ÀÜ¾×: " << my_money << endl;
}