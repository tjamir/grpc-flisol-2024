import grpc 
import api_pb2, api_pb2_grpc
import sys
from datetime import datetime

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = api_pb2_grpc.ClientBankServiceStub(channel)
        
        def show_menu():
            print("1. Transfer")
            print("2. Show Bank Statement")
            print("3 Exit")
            choice = int(input("Enter your choice: "))
            return choice
        
        def transfer():
            source = input("your account id: ")
            dest = input("destination account id: ")
            amount = float(input("amount: "))
            password = input("password: ")

            try:
                resp  = stub.Transfer(api_pb2.TransferRequest(sourceAccountId=source, targetAccountId=dest, password=password, value=amount))
                print("transfer successful")
                transaction = resp.transaction
                print("transaction ")
                print_transaction(transaction)
                print("balance ", resp.accountBalance)
            except grpc.RpcError as e:
                print("deposit failed")
                print(e)
        
        def print_transaction(transaction):
            id = transaction.id
            amount = transaction.amount
            time = transaction.time
          

            timestamp_dt = datetime.fromtimestamp(time.seconds + time.nanos/1e9)
            time_str = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
            line = f"{id} {amount} {time_str}"
            print(line)
        def bank_statement():
            accountId = input("account id: ")
            password = input("password: ")
            try:
                resp = stub.Statement(api_pb2.BankStatementRequest(accountId=accountId, password=password))
                print("bank statement")
                for transaction in resp.transactions:
                    print_transaction(transaction)
                print(f"balance {resp.amount}")
            except grpc.RpcError as e:
                print("bank statement failed")
                print(e)
            

        while True:
            choice = show_menu()
            if choice == 1:
                transfer()
            elif choice == 2:
                bank_statement()
            elif choice == 3:
                break
            else:
                print("invalid choice")
                    


if __name__ == '__main__':
    run()