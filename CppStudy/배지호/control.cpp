#include "control.h"

void show_menu()
{
	cout << "-------------Menu------------" << endl;
	cout << "1. 계좌개설" << endl;
	cout << "2. 입 금" << endl;
	cout << "3. 출 금" << endl;
	cout << "4. 계좌정보 전체 출력" << endl;
	cout << "5. 프로그램 종료" << endl;
}

int find_id(Account* customer[], int account_count, int id)
{
	for (int i = 0; i < account_count; i++)
	{
		if (customer[i]->compare_id(id) == 1)    // compare_id(id) id값과 클래스의 id값이 일치하면 1반환
			return i;
	}
	cout << "해당 id가 없습니다." << endl;

	return -1;
}

void make_account(Account* customer[], int& account_count)
{
	int id;
	char name[20];
	int money = 0;

	cout << "[계좌개설]" << endl;
	cout << "계좌ID: ";
	cin >> id;
	cout << "이름: ";
	cin >> name;
	cout << "입금액: ";
	cin >> money;

	customer[account_count] = new Account(id, name, money);
	account_count++;

	cout << "계좌개설 완료" << endl;

	return;
}

void deposit(Account* customer[], int& account_count)
{
	int id;
	int money = 0;
	int customer_index;

	cout << "[입 금]" << endl;
	cout << "계좌ID: ";
	cin >> id;
	cout << "입금액: ";
	cin >> money;

	customer_index = find_id(customer, account_count, id);	//입력 id에 해당하는 클래스의 포인터배열 인덱스 반환

	if (customer_index == -1)								// 일치하는 id를 못찾았을때
		return;

	customer[customer_index]->add_money(money);

	cout << "입금 완료" << endl;

	return;
}

void withdraw(Account* customer[], int& account_count)
{
	int id;
	int money = 0;
	int customer_index;

	cout << "[출 금]" << endl;
	cout << "계좌ID: ";
	cin >> id;
	cout << "출금액: ";
	cin >> money;

	customer_index = find_id(customer, account_count, id);    //입력 id에 해당하는 클래스의 포인터배열 인덱스 반환

	if (customer_index == -1)                                 // 일치하는 id를 못찾았을때
		return;

	customer[customer_index]->add_money();

	cout << "출금 완료" << endl;

	return;
}

void show_all_customer(Account* customer[], int& account_count)
{
	cout << endl;
	cout << "[계좌정보]" << endl;

	for (int i = 0; i < account_count; i++)
	{
		customer[i]->show_cus();
	}

	cout << endl;

	return;
}