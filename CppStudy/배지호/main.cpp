#include "account.h"
#include "control.h"

int main()
{
	int n;
	int account_count = 0;
	
	Account* customer[100];

	while (1) {
		show_menu();      //메뉴 출력
		cout << "선택: ";
		cin >> n;

		switch (n)
		{
		case 1:
			make_account(customer, account_count);   //계좌 개설
			break;
		case 2:
			deposit(customer, account_count);    // 입금
			break;
		case 3:
			withdraw(customer, account_count);  //출금 
			break;
		case 4:
			show_all_customer(customer, account_count); //계좌정보 전체출력
			break;
		case 5:
			cout << "프로그램 종료" << endl;
			for (int i = 0; i < account_count; i++)     //메모리 해제
				delete customer[i];
			return 0;
		default:
			cout << "해당 번호 없음" << endl;
			return -1;
		}
	}

	return 0;
}






