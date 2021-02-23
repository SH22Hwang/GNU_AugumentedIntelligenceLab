#include <iostream>
#include <cstring>
using namespace std;

char all_ID[];
int idNum = 1;

class  Account {
private:
    int ID;
    char* Name;
    int Money;
public:
    Account(int newID, char* newName, int newMoney) : ID(newID), Money(newMoney) {
        Name = new char[strlen(newName) + 1];
        strcpy(Name, newName);
    }

    // 계좌 개설
    void NewAccount(int newID, char* newName, int newMoney) {
        Name = new char[strlen(newName) + 1];
        strcpy(Name, newName);
        Money = newMoney;
        ID = newID;

        all_ID[idNum] = newID;   // ID 넣어주는 배열
        idNum++;

        cout << "[계좌개설]" << endl;
        cout << "계좌ID: "; cin >> newID;
        cout << "이 름: "; cin >> newName;
        cout << "입금액: "; cin >> newMoney;
    }

    // 입금
    void InMoney(int newID, int newMoney) {
        for (int i = 0; i < 10; i++) {   // 10개로 한정....^^...
            if (all_ID[i] == newID) {   // ID 존재O

                cout << "[입" << '\t' << "금]" << endl;
                cout << "계좌ID: "; cin >> newID;
                cout << "입금액: "; cin >> newMoney;
                Money += newMoney;
                cout << "입금완료" << endl;
            }
            else {
                cout << "찾으시는 계좌ID가 존재하지 않습니다." << endl;   // ID 존재X
            }
        }
    }

    // 출금
    void OutMoney(int newID, int newMoney) {
        for (int i = 0; i < 10; i++) {
            if (all_ID[i] == newID) {

                cout << "[출" << '\t' << "금]" << endl;
                cout << "계좌ID: "; cin >> newID;
                cout << "출금액: "; cin >> newMoney;
                if (Money < newMoney) {   // 해당 ID의 잔고보다 출금액이 큰 경우
                    cout << "잔고가 부족합니다" << endl;
                }
                else {
                    Money -= newMoney;
                    cout << "출금완료" << endl;
                }
            }
            else {
                cout << "찾으시는 계좌ID가 존재하지 않습니다." << endl;
            }
        }
    }

    ~Account() {
        delete[]Name;   // 동적할당 해제
    }
};

void ShowMenu() {
    cout << "-----Menu-----" << endl;
    cout << "1. 계좌개설" << endl;
    cout << "2. 입 금" << endl;
    cout << "3. 출 금" << endl;
    cout << "4. 계좌정보 전체 출력" << endl;
    cout << "5. 프로그램 종료" << endl;
}

void ChooseMenu(int menu) {
    switch (menu) {
    case 1:
        Account NewAccount();
        break;
    case 2:
        Account InMoney();
        break;
    case 3:
        Account OutMoney();
        break;
    case 4:
        Account ShowAllAccount();   // 구현X
        break;
    case 5:
        exit(0);
    }
}

int main() {
    int menu;

    while (1) {
        ShowMenu();
        cout << "선택: ";
        cin >> menu;
        cout << endl;

        if (menu > 0 && menu < 6) {
            ChooseMenu(menu);
        }
        else {
            cout << "다시 입력하세요" << endl;
            ShowMenu();      // 111-114와 코드 중복
            cout << "선택: ";
            cin >> menu;
            cout << endl;
        }
    }
    return 0;
}