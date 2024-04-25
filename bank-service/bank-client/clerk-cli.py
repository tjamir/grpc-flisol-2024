import grpc 
import api_pb2, api_pb2_grpc
import sys
from datetime import datetime

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = api_pb2_grpc.ClerkBankServiceStub(channel)

        def show_menu():
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4 Exit")
            choice = int(input("Enter your choice: "))
            return choice
        
        def deposit():
            accountid = input("account id: ")
            amount = float(input("amount: "))
            try:
                resp  = stub.DoTransaction(api_pb2.TransactionRequest(accountId=accountid, amount=amount, action=api_pb2.ACTION_DEPOSIT))
                print("deposit successful")
                transaction = resp.transaction
                print("transaction")
                print_transaction(transaction)
                print("balance ", resp.accountBalance)
            except grpc.RpcError as e:
                print("deposit failed")
                print(e)
            

        def withdraw():

            accountid = input("account id: ")
            amount = float(input("amount: "))
            try:
                resp  = stub.DoTransaction(api_pb2.TransactionRequest(accountId=accountid, amount=amount, action=api_pb2.ACTION_WITHDRAWAL))
                print("withdraw successful")
                transaction = resp.transaction
                print("transaction")
                print_transaction(transaction)
                print("balance ", resp.accountBalance)
            except grpc.RpcError as e:
                print("withdraw failed")
                print(e)
        
        def create_account():
            name = input("name: ")
            password = input("password: ")
            try:
                resp  = stub.CreateAccount(api_pb2.CreateAccountRequest(name=name, password=password))
                print("account created")
                account = resp.accountId
                print("account ", account)
            except grpc.RpcError as e:
                print("account creation failed")
                print(e)

        def print_transaction(transaction):
            id = transaction.id
            amount = transaction.amount
            time = transaction.time
          

            timestamp_dt = datetime.fromtimestamp(time.seconds + time.nanos/1e9)
            time_str = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
            line = f"{id} {amount} {time_str}"
            print(line)

        while True:
            choice = show_menu()
            if choice == 1:
                create_account()
            elif choice == 2:
                deposit()
            elif choice == 3:
                withdraw()
            elif choice == 4:
                break
            else:
                print("invalid choice")
                continue



        
            



if __name__ == '__main__':
    run()