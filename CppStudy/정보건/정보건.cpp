#include <iostream>
#include <cstring>

using namespace std;
const int NAME_LEN = 10; //이름 길이 제한

void newacoount(void);
void putaccount(void);
void outaccount(void);
void showallacoount(void);
void getoutprogram(void);
void showmenu(void);

enum {new=1,put,out,showall,getout};

class acoount
{
private:
   int accountid;//계좌번호
   int extra;//잔액
   char custname;//사용자이름

public:
   account(int accountid, int extra, char custname)
   
};

int main(void)
{
   int select;

   while (1)
   {
      showmenu();
      cout << "선택: " << endl;
      cin >> select;
      cout << endl;

      switch (select)
      {
      case new:
         newacoount();
         break;
      case put:
         putaccount();
         break;
      case out:
         outaccount();
         break;
      case showall:
         showallacoount();
         break;
      case getout:
         getoutprogram();
         break;
      default:
         cout << "잘못 선택하셨습니다." << endl;
      }
      
   }
   return 0;
}

void showmenu(void)
{
   cout << "----------MENU----------" << endl;
   cout << "1. 계좌개설" << endl;
   cout << "2. 입금" << endl;
   cout << "3. 출금" << endl;
   cout << "4. 계좌정보 전체 출력" << endl;
   cout << "5. 프로그램 종료" << endl;
}

void newaccount(void)
{
   int id;
   char name[NAME_LEN];
   int money;

   cout << "[계좌개설]" << endl;
   cout << "계좌ID : "; cin >> id;
   cout << "이름 : "; cin >> name;
   cout << "입금액 : "; cin >> money;
   cout << endl;
}

void putaccount(void)
{
   int i
}

void outaccount(void)
{

}

void showallacount(void)
{

}

void getoutprogram(void)
{

}