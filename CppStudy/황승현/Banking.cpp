#include "Banking.h"
#include <cstring>

#define ACCOUNT_LENTH 999

Account* accArr[ACCOUNT_LENTH];
int accNum = 0;

void Account::Init() {
	accId = -1;
	balance = -1;
}

int Account::GetId() {
	return accId;
}
char* Account::GetName() {
	return cusName;
}

int Account::GetBalance() {
	return balance;
}

void Account::DepositAcc(int money) {
	balance += money;
}

void Account::WithdrawalAcc(int money) {
	balance -= money;
}

// bool Account::SetId(int id) {
//	 if (id < 0 || id > 999) {
//		 cout << "잘못된 범위" << endl;
//		 return false;
//	 }
//	 
//	 acc[id].accId = id;
//
//	 return true;
//}
//
// bool Account::SetName(char* name[]) { // 책 참고
//	 strcpy_s(acc[id].name, name);
//}
//
// bool Account::SetMoney() {
//	 if (balance < 0) {
//		 cout << "잘못된 범위" << endl;
//		 return false;
//	 }
//
//	 acc[accId].balance = balance;
//
//	 return true;
//}

void ShowMenu() {
	cout << "-----Menu-----\n"
		<< "1. 계좌개설\n"
		<< "2. 입급\n"
		<< "3. 출금\n"
		<< "4. 전체 고객 조회"
		<< endl;
}

void OpenAccount() {
	int id = 0;
	char name[20];
	int balance;

	cout << "[계좌 개설]\n";
	cout << "id: ";
	cin >> id;

	cout << "이름: ";
	cin >> name;

	cout << "입금액: ";
	cin >> balance;

	accArr[accNum++] = new Account(id, balance, name);
}

void Deposit() {
	int id, money;
	cout << "[입금]\n";
	cout << "id: ";
	cin >> id;
	cout << "입금할 금액: ";
	cin >> money;

	for (int i = 0; i < accNum; i++) {
		if (accArr[i]->GetId() == id) { // 포인터인듯
			accArr[i]->DepositAcc(money);
			cout << "입금 완료" << endl;
			return;
		}
	}
	cout << "없는 ID" << endl;
}

void Withdrawal() {
	int id, money;
	cout << "[출금]\n";
	cout << "id: ";
	cin >> id;
	cout << "출금할 금액: ";
	cin >> money;

	for (int i = 0; i < accNum; i++) {
		if (accArr[i]->GetId() == id) { // 포인터인듯
			accArr[i]->WithdrawalAcc(money);
			cout << "출금 완료" << endl;
			return;
		}
	}
	cout << "없는 ID" << endl;
}

void ShowAllAcc() {
	cout << "[전체 고객 조회]\n";
	for (int i = 0; i < accNum; i++) {
		cout
			<< "사용자 id: " << accArr[i]->GetId()
			<< "\n사용자 이름: " << accArr[i]->GetName()
			<< "\n잔액: " << accArr[i]->GetBalance()
			<< endl << endl;
	}
}