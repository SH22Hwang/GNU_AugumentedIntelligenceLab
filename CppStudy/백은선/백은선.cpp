#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <cstring>
#define NAME_LEN 20

using namespace std;

void ShowMenu(void);         //메뉴출력
void MakeAccount(void);         //계좌개설
void DepositMoney(int money);      //입금
void WithdrawMoney(int money);      //출금
void AllAccount(void);      //계좌정보 전체 출력

class Account
{
private:
    int accID;      //계좌번호
    char* accName;   //고객이름
    int accMoney;   //잔액

public:
    Account(int id, char* name, int money) : accID(id), accMoney(돈) //생성자
    {
        accName = new char[strlen(name) + 1];
        strcpy(accName, name);
    }

    int GetAccID() { return accID; }

    void Deposit(int Money)
    {
        accMoney += Money;
    }

    int Withdraw(int Money)
    {
        if (accMoney < Money)
            return 0;

        accMoney -= Money;
        return Money;
    }

    void ShowAccInfo()
    {
        cout << "계좌ID: " << accID << endl;
        cout << "이름: " << accName << endl;
        cout << "잔액: " << accMoney << endl;
    }

    ~Account()   //소멸자
    {
        delete[]accName;
    }
};

Account* accArr[100];   //계좌 포인터 배열
int accNum = 0;         //계좌 개수



int main(void) {

    int choice, money;

    while (true) {
        ShowMenu();
        cout << "선택: ";
        cin >> choice;
        cout << endl;

        switch (choice) {
        case 1:   //계좌 개설
            MakeAccount();
            break;
        case 2:   //입금
            cout << "입급할 금액: ";
            cin >> money;
            cout << endl;
            DepositMoney(돈);
            break;
        case 3:   //출금
            cout << "출금할 금액: ";
            cin >> money;
            cout << endl;
            WithdrawMoney(돈);
            break;
        case 4:   //전체 출력
            AllAccount();
            break;
        case 5:
            for (int i = 0; i < accNum; i++)   //포인터배열을 동적할당했으므로
                delete accArr[i];
            return 0;
        default:
            cout << "잘못된 번호 입력" << endl << endl;
        }

    }
    return 0;
}

void ShowMenu(void) {

    cout << "-------Menu-------" << endl;
    cout << "1. 계좌 개설" << endl;
    cout << "2. 입금" << endl;
    cout << "3. 출금" << endl;
    cout << "4. 계좌정보 전체 출력" << endl;
    cout << "5. 프로그램 종료" << endl;
    cout << "-----------------" << endl << endl;
}


void MakeAccount(void) {   //계좌개설

    int id;
    char name[NAME_LEN];
    int money;

    cout << "[ 계좌 개설 ]" << endl;
    cout << "계좌ID: "; cin >> id;
    cout << "이름: "; cin >> name;
    cout << "입금액: "; cin >> money;
    cout << endl;

    accArr[accNum++] = new Account(id, name, money);   //생성자에 데이터 전달
}


void DepositMoney(int money) {      //입금

    int id;
    cout << "[ 입  금 ]" << endl;
    cout << "계좌ID: ";
    cin >> id;
    cout << "입금액: " << money << endl;;

    for (int i = 0; i < accNum; i++) {
        if (accArr[i]->GetAccID() == id)
        {
            accArr[i]->Deposit(돈);
            cout << "입금완료" << endl << endl;
            return;
        }
    }

    cout << "유효하지않은 ID 입니다." << endl << endl;
}


void WithdrawMoney(int money) {      //출금
    int id;
    cout << "[ 출  금 ]" << endl;
    cout << "계좌ID: ";
    cin >> id;
    cout << "출금액: " << money << endl;;

    for (int i = 0; i < accNum; i++) {
        if (accArr[i]->GetAccID() == id) {

            if (accArr[i]->Withdraw(돈) == 0) {
                cout << "잔액부족" << endl << endl;
                return;
            }
            cout << "출금완료" << endl << endl;
            return;
        }
    }

    cout << "유효하지않은 ID 입니다." << endl << endl;
}


void AllAccount(void) {      //계좌정보 전체 출력
    cout << "[ 계좌정보 전체 출력 ]" << endl;

    for (int i = 0; i < accNum; i++) {
        accArr[i]->ShowAccInfo();
        cout << endl;
    }


}