#pragma once
#include"account.h"

void show_menu();				//메뉴출력
int find_id(Account* customer[], int account_count, int id);	//id 검색
void make_account(Account* customer[], int& account_count);     //계좌 개설
void deposit(Account* customer[], int& account_count);			//입금
void withdraw(Account* customer[], int& account_count);			//출금
void show_all_customer(Account* customer[], int& account_count); //계좌정보 전체 출력